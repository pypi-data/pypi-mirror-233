# pylint: disable=C0415
import asyncio
import json
import logging
import os
import random
import threading
import time
from datetime import date, datetime, timedelta

import httpx
from dateutil import tz
from fastapi import WebSocket
from httpx import ConnectTimeout, ReadTimeout
from pydantic import ValidationError

from ..logging.app_logger import write_external_service_data
from ..services.data_validator import capitalize_custom
from ..services.mock_data import get_mock_managed_meeting_points, get_mock_slots
from .application import Application
from .municipality import Municipality

FRA_TZ = tz.gettz("Europe/Paris")


class Editor:
    slug: str
    name: str
    api_url: str
    _test_mode: bool
    status: bool
    api_down_datetime: datetime
    api_up_datetime: datetime

    def __init__(
        self,
        slug: str,
        name: str,
        api_url: str,
        test_mode: bool,
        status: bool = True,
        api_down_datetime: datetime = None,
        api_up_datetime: datetime = None,
    ):
        self.slug = slug
        self.name = name
        self.api_url = api_url
        self._test_mode = test_mode
        self.status = status
        self.api_down_datetime = api_down_datetime
        self.api_up_datetime = api_up_datetime

    async def get_managed_meeting_points(self):
        _logger = logging.getLogger("root")
        await asyncio.sleep(0.00001)
        points = []
        if self._test_mode:
            points = get_mock_managed_meeting_points(self)
        else:
            try:
                headers = {
                    "x-hub-rdv-auth-token": os.environ.get(f"{self.slug}_auth_token")
                }
                async with httpx.AsyncClient(verify=False) as async_client:
                    response = await async_client.get(
                        f"{self.api_url}/getManagedMeetingPoints",
                        headers=headers,
                        timeout=20,
                        follow_redirects=True,
                    )
                    write_external_service_data(
                        _logger, response, editor_name=self.name
                    )
                    if response.status_code in [200]:
                        self.api_up_datetime = datetime.now(tz=FRA_TZ)
                        if not self.status:
                            self.status = True

                        points = response.json()
                    else:
                        raise Exception(
                            f"Status code not handled : {response.status_code}"
                        )
            except Exception as get_meeting_points_e:
                if self.status:
                    self.status = False
                    self.api_down_datetime = datetime.now(tz=FRA_TZ)

                _logger.error(
                    "Error while getting meeting points for %s : %s",
                    self.name,
                    str(get_meeting_points_e),
                    extra={"extra_info": {"type": "app", "editor_name": self.name}},
                )

                retry_thread = [
                    th
                    for th in threading.enumerate()
                    if th.name == f"retry-get-managed-{self.name}"
                ]
                if len(retry_thread) < 1:
                    retry_thread = threading.Thread(
                        target=self.retry_get_managed_meeting_points,
                        name=f"retry-get-managed-{self.name}",
                    )
                    retry_thread.start()

        valid_meeting_points = []
        for point in points:
            try:
                point["_editor_name"] = self.name
                point["_internal_id"] = str(point["id"])
                point["city_name"] = capitalize_custom(point["city_name"])
                if (
                    point["zip_code"]
                    and point["public_entry_address"]
                    and (point["zip_code"] in point["public_entry_address"])
                ):
                    point["public_entry_address"] = point["public_entry_address"][
                        : point["public_entry_address"].index(point["zip_code"])
                    ].strip()
                point["zip_code"] = point["zip_code"] and point["zip_code"].strip()
                Municipality.parse_obj(point)
                valid_meeting_points.append(point)
            except ValidationError as meeting_point_validation_e:
                _logger.error(
                    "Error while validating meeting point : %s \nError: %s",
                    point,
                    meeting_point_validation_e,
                    extra={"extra_info": {"type": "app", "editor_name": self.name}},
                )
            except Exception as validation_unknown_e:
                _logger.error(
                    "Error while validating meeting point : %s \nError: %s",
                    point,
                    validation_unknown_e,
                    extra={"extra_info": {"type": "app", "editor_name": self.name}},
                )

        return valid_meeting_points

    async def get_available_time_slots(
        self, meeting_points, start_date, end_date, reason="CNI", documents_number=1
    ):
        _logger = logging.getLogger("root")
        # this sleep is necessary to not block other async operations
        await asyncio.sleep(0.00001)
        result = {}
        editor_error = None
        response = None

        def last_day_of_month(any_day):
            next_month = any_day.replace(day=28) + timedelta(days=4)
            return (next_month.replace(day=1) - timedelta(days=1)).day

        # start_date and end_date should be fixed to help editors handle their cache
        monthly_start_date = None
        monthly_end_date = None
        try:
            monthly_start_date = start_date.replace(
                day=date.today().day if start_date.month == date.today().month else 1
            )
            monthly_end_date = end_date.replace(day=last_day_of_month(end_date))
        except Exception as monthly_date_e:
            _logger.error(
                "Error while creating monthly search dates: %s",
                monthly_date_e,
                extra={"extra_info": {"type": "app"}},
            )

        if self._test_mode:
            await asyncio.sleep(random.randint(3, 12))
            for meeting_point in meeting_points:
                meeting_point_slots = get_mock_slots(
                    meeting_point, start_date, end_date
                )
                result[meeting_point["_internal_id"]] = meeting_point_slots
        else:
            meeting_point_ids = [x["_internal_id"] for x in meeting_points]
            try:
                headers = {
                    "x-hub-rdv-auth-token": os.environ.get(f"{self.slug}_auth_token")
                }
                parameters = {
                    "start_date": monthly_start_date or start_date or date.today(),
                    "end_date": monthly_end_date
                    or end_date
                    or (date.today() + timedelta(days=150)),
                    "meeting_point_ids": meeting_point_ids,
                    "reason": reason,
                    "documents_number": documents_number,
                }
                async with httpx.AsyncClient(verify=False) as async_client:
                    response = await async_client.get(
                        f"{self.api_url}/availableTimeSlots",
                        headers=headers,
                        params=parameters,
                        timeout=15,
                        follow_redirects=True,
                    )
                    write_external_service_data(_logger, response, self.name)
                    if response.status_code in [200]:
                        self.api_up_datetime = datetime.now(tz=FRA_TZ)
                        if not self.status:
                            self.status = True
                            self.api_down_datetime = datetime.now(tz=FRA_TZ)

                        result = response.json()
                    else:
                        raise Exception(
                            f"Status code not handled : {response.status_code} : {response.reason_phrase}"
                        )
            except ReadTimeout:
                if self.status:
                    self.status = False
                    self.api_down_datetime = datetime.now(tz=FRA_TZ)

                _logger.error(
                    "Timeout while getting available time slots for %s",
                    self.name,
                    extra={
                        "extra_info": {
                            "type": "app",
                            "editor_name": self.name,
                            "category": "external_service",
                            "endpoint": "availableTimeSlots",
                        }
                    },
                )
            except ConnectTimeout:
                if self.status:
                    self.status = False
                    self.api_down_datetime = datetime.now(tz=FRA_TZ)

                _logger.error(
                    "Connexion Timeout while getting available time slots for %s",
                    self.name,
                    extra={
                        "extra_info": {
                            "type": "app",
                            "editor_name": self.name,
                            "category": "external_service",
                            "endpoint": "availableTimeSlots",
                        }
                    },
                )
            except Exception as available_time_slots_e:
                if self.status:
                    self.status = False
                    self.api_down_datetime = datetime.now(tz=FRA_TZ)

                _logger.error(
                    "Error while getting available time slots for %s : %s",
                    self.name,
                    str(available_time_slots_e),
                    extra={
                        "extra_info": {
                            "type": "app",
                            "parameters": {
                                "start_date": str(parameters["start_date"]),
                                "end_date": str(parameters["end_date"]),
                                "meeting_point_ids": parameters["meeting_point_ids"],
                                "reason": parameters["reason"],
                                "documents_number": parameters["documents_number"],
                            },
                            "editor_name": self.name,
                            "category": "external_service",
                            "endpoint": "availableTimeSlots",
                        }
                    },
                )
                editor_error = {"error": available_time_slots_e, "editor": self.name}

        if (not start_date) and (not end_date):
            return result, None

        filtered_dates_result = {}
        try:
            for meeting_point_id in result:
                filtered_dates_result[meeting_point_id] = []
                for available_timeslot in result[meeting_point_id]:
                    timeslot_datetime = None
                    for datetime_format in ["%Y-%m-%dT%H:%MZ", "%Y-%m-%dT%H:%M:%S%z"]:
                        try:
                            timeslot_datetime = datetime.strptime(
                                available_timeslot["datetime"], datetime_format
                            )
                            if timeslot_datetime.tzinfo:
                                utcoffset = (
                                    timeslot_datetime.utcoffset().total_seconds()
                                    / 60
                                    / 60
                                )
                                timeslot_datetime = timeslot_datetime.replace(
                                    tzinfo=None
                                ) + timedelta(hours=utcoffset)
                            break
                        except ValueError:
                            pass
                    if (
                        (not timeslot_datetime)
                        or (start_date and (timeslot_datetime.date() < start_date))
                        or (end_date and (timeslot_datetime.date() > end_date))
                    ):
                        _logger.debug(
                            "[%s] DATE OUT OF RANGE : %s",
                            self.name,
                            str(timeslot_datetime),
                        )
                    else:
                        filtered_dates_result[meeting_point_id].append(
                            {
                                "datetime": timeslot_datetime.strftime(
                                    "%Y-%m-%dT%H:%M:%SZ"
                                ),
                                "callback_url": available_timeslot["callback_url"],
                            }
                        )
        except Exception as checking_date_filter_e:
            _logger.error(
                "[%s] Checking date filter error : %s",
                self.name,
                str(checking_date_filter_e),
                extra={"extra_info": {"type": "app", "editor_name": self.name}},
            )
            editor_error = {"error": checking_date_filter_e, "editor": self.name}
        return filtered_dates_result, editor_error

    async def search_slots_in_editor(
        self,
        meeting_points,
        start_date,
        end_date,
        reason="CNI",
        documents_number=1,
        websocket: WebSocket = None,
    ):
        # this sleep is necessary to not block other async operations
        time.sleep(0.00001)
        editor_error = None
        editor_meeting_points = []
        editor_meeting_points_with_slots = []
        for meeting_point in meeting_points:
            if meeting_point["_editor_name"] == self.name:
                editor_meeting_points.append(meeting_point)
        if editor_meeting_points:
            slots, editor_error = await self.get_available_time_slots(
                editor_meeting_points, start_date, end_date, reason, documents_number
            )
            for meeting_point in editor_meeting_points:
                if (
                    meeting_point["_internal_id"] in slots
                    and slots[meeting_point["_internal_id"]]
                ):
                    meeting_point["available_slots"] = slots[
                        meeting_point["_internal_id"]
                    ]
                    editor_meeting_points_with_slots.append(meeting_point)
            if websocket:
                safe_editor_meeting_points_with_slots = []
                for editor_meeting_point_with_slots in editor_meeting_points_with_slots:
                    editor_meeting_point_with_slots_copy = (
                        editor_meeting_point_with_slots.copy()
                    )
                    if "_editor_name" in editor_meeting_point_with_slots_copy:
                        del editor_meeting_point_with_slots_copy["_editor_name"]
                    if "_internal_id" in editor_meeting_point_with_slots_copy:
                        del editor_meeting_point_with_slots_copy["_internal_id"]
                    safe_editor_meeting_points_with_slots.append(
                        editor_meeting_point_with_slots_copy
                    )
                json_string = json.dumps(
                    safe_editor_meeting_points_with_slots, default=str
                )
                await websocket.send_text(json_string)
        return editor_meeting_points_with_slots, editor_error

    async def search_meetings(self, application_ids):
        _logger = logging.getLogger("root")
        await asyncio.sleep(0.00001)
        meetings = {}
        if not self._test_mode:
            try:
                headers = {
                    "x-hub-rdv-auth-token": os.environ.get(f"{self.slug}_auth_token")
                }
                parameters = {"application_ids": application_ids}
                async with httpx.AsyncClient(verify=False) as async_client:
                    response = await async_client.get(
                        f"{self.api_url}/searchApplicationIds",
                        headers=headers,
                        params=parameters,
                        timeout=5,
                        follow_redirects=True,
                    )
                    write_external_service_data(_logger, response, self.name)
                    if response.status_code in [200]:
                        meetings = response.json()
                    else:
                        raise Exception(
                            f"Status code not handled : {response.status_code} : {response.reason_phrase}"
                        )
            except Exception as search_meetings_e:
                _logger.error(
                    "Error while seachring meetings by application ID for %s : %s",
                    self.name,
                    str(search_meetings_e),
                    extra={"extra_info": {"type": "app", "editor_name": self.name}},
                )
        else:
            await asyncio.sleep(random.randint(3, 5))

        valid_meetings = {}
        for applicationId in meetings:
            valid_meetings[applicationId] = []
            for meeting in meetings[applicationId]:
                try:
                    Application.parse_obj(meeting)
                    valid_meetings[applicationId].append(meeting)
                except ValidationError as meeting_validation_e:
                    _logger.error(
                        "Error while validating meeting : %s \nError: %s",
                        meeting,
                        meeting_validation_e,
                        extra={"extra_info": {"type": "app", "editor_name": self.name}},
                    )
        return valid_meetings

    def retry_get_managed_meeting_points(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        result = loop.run_until_complete(self._retry_get_managed_meeting_points())
        loop.close()

        return result

    async def _retry_get_managed_meeting_points(self):
        _logger = logging.getLogger("root")

        counter = 0
        while counter < 60 * 20:
            time.sleep(1 * 60)
            try:
                meeting_points = await self.get_managed_meeting_points()
                if meeting_points:
                    from ..db.utils import (
                        get_all_meeting_points,
                        set_all_meeting_points,
                    )

                    all_meeting_points = get_all_meeting_points()
                    all_meeting_points += meeting_points
                    set_all_meeting_points(all_meeting_points)
                    break
                else:
                    raise Exception(f"No meeting points found for editor {self.name}")
            except Exception as retry_get_managed_meeting_points_e:
                _logger.error(
                    "Error while retrying to get managed meeting for editor %s : %s",
                    self.name,
                    retry_get_managed_meeting_points_e,
                    extra={"extra_info": {"type": "app"}},
                )
            counter += 1

        _logger.info(
            "End of retrying to get managed meeting points for editor %s",
            self.name,
            extra={"extra_info": {"type": "app"}},
        )


def init_all_editors():
    citopia_editor = Editor(
        "citopia", "Citopia", "https://pro.rendezvousonline.fr/api", False, True
    )
    synbird_editor = Editor(
        "synbird", "Synbird", "https://sync.synbird.com/ants", False, True
    )
    esii_editor = Editor(
        "esii", "ESII", "https://api.esii-orion.com/ants/api/public/1/ants", False, True
    )
    troov_editor = Editor("troov", "Troov", "https://api.troov.com/api", False, True)
    rdv_360_editor = Editor(
        "rdv360", "RDV360", "https://ants.rdv360.com/api", False, True
    )
    ypok_editor = Editor(
        "ypok", "Ypok", "https://yservice.ypok.com/api.php", False, True
    )
    solocal_editor = Editor(
        "solocal", "Solocal", "https://api.solocal.com/v1/ants", False, True
    )
    smartagenda_editor = Editor(
        "smartagenda",
        "SmartAgenda",
        "https://interfaces.smartagenda.fr/partenaires/ants/",
        False,
        True,
    )
    numesia_editor = Editor(
        "numesia", "Numesia", "https://rdvs-ants.mon-guichet.fr/api", False, True
    )
    info_local_editor = Editor(
        "infolocal", "InfoLocale", "https://api.rdvenmairie.fr/api", False, True
    )
    agglocompiegne_editor = Editor(
        "agglocompiegne",
        "AggloCompiegne",
        "https://demarches.agglo-compiegne.fr/api",
        False,
        True,
    )
    aggloroyan_editor = Editor(
        "aggloroyan",
        "AggloRoyan",
        "https://api.agglo-royan.fr/rdv-ci",
        False,
        True,
    )
    soultz_editor = Editor(
        "soultzsousforet",
        "Soultz-sous-Forêt",
        "https://www.soultzsousforets.fr/api",
        False,
        True,
    )
    kembs_editor = Editor(
        "kembs",
        "Kembs",
        "https://www.kembs.fr/api",
        False,
        True,
    )
    un23mairie_editor = Editor(
        "un23mairie",
        "123Mairie",
        "https://rdv.123mairie.net/api",
        False,
        True,
    )
    vernalis_editor = Editor(
        "vernalis",
        "Vernalis",
        "https://proxyants.vernalis.fr/api/rdv/v1",
        False,
        True,
    )
    creasit_editor = Editor(
        "creasit",
        "Creasit",
        "https://proxy-ants.creasit.com/api",
        False,
        True,
    )
    esii_onpremise_editor = Editor(
        "esiionpremise",
        "ESII on premise",
        "https://horus-api.azure-api.net/api",
        False,
        True,
    )
    agendize_editor = Editor(
        "agendize", "Agendize", "https://connect2.agendize.com/api", False, True
    )
    anct_editor = Editor(
        "anct",
        "ANCT",
        "https://rdv.anct.gouv.fr/api/ants",
        False,
        True,
    )
    entrouvert_editor = Editor(
        "entrouvert",
        "Entrouvert",
        "https://hub-ants.entrouvert.org/api/ants",
        False,
        True,
    )
    convergence_editor = Editor(
        "convergence",
        "Convergence",
        "https://web5.gie-convergence.fr",
        False,
        True,
    )
    arpege_editor = Editor(
        "arpege",
        "Arpège",
        "https://rdv.espace-citoyens.net/frontal-rdv-restitution/api",
        False,
        True,
    )
    wittisheim_editor = Editor(
        "wittisheim",
        "Wittisheim",
        "https://www.wittisheim.fr/api",
        False,
        True,
    )
    pecq_editor = Editor(
        "pecq",
        "Pecq",
        "https://pecq.fr.qmatic.cloud/ants-integration/api",
        False,
        True,
    )
    lorient_editor = Editor(
        "lorient",
        "Lorient",
        "https://rdv.lorient.bzh/ants-integration/api",
        False,
        True,
    )
    neuville_sur_saone_editor = Editor(
        "neuville_sur_saone",
        "Neuville-sur-Saône",
        "https://www.mairie.neuvillesursaone.fr/api",
        False,
        True,
    )
    pont_saint_esprit_editor = Editor(
        "pontsaintesprit",
        "Pont saint esprit",
        "https://pont-saint-esprit-grc.e-citiz.com/SEWSaaS.TS.Reservation/ANTS/api",
        False,
        True,
    )
    saint_etienne_du_rouvray_editor = Editor(
        "saintetiennedurouvray",
        "Saint Etienne du Rouvray",
        "https://demarches.saintetiennedurouvray.fr/SEWSaaS.TS.Reservation/ANTS/api",
        False,
        True,
    )
    mobminder_editor = Editor(
        "mobminder",
        "Mobminder",
        "https://fr.mobminder.com/ants",
        False,
        True,
    )
    boisseuil_editor = Editor(
        "boisseuil",
        "Boisseuil",
        "https://rdvcnipass.boisseuil87.fr/api",
        False,
        True,
    )
    espace_rendez_vous_1_editor = Editor(
        "espacerendezvous1",
        "Espace rendez-vous 1",
        "https://ants1.espacerendezvous.com/espaceRdvServer/api",
        False,
        True,
    )
    espace_rendez_vous_2_editor = Editor(
        "espacerendezvous2",
        "Espace rendez-vous 2",
        "https://ants2.espacerendezvous.com/espaceRdvServer/api",
        False,
        True,
    )
    gallia_editor = Editor(
        "gallia",
        "Gallia",
        "https://www.gallia-demarches.fr/ants/api",
        False,
        True,
    )
    mourmelon_le_grand_editor = Editor(
        "mourmelon_le_grand",
        "Mourmelon-le-grand",
        "https://rdv.mourmelonlegrand.fr/api",
        False,
        True,
    )
    meze_editor = Editor(
        "meze",
        "Mèze",
        "https://rdv.ville-meze.fr/api",
        False,
        True,
    )
    aiguillon_editor = Editor(
        "aiguillon",
        "Aiguillon",
        "https://www.ville-aiguillon.fr/api",
        False,
        True,
    )
    plerin_editor = Editor(
        "plerin",
        "Plérin",
        "https://plerin-sur-mer-grc.e-citiz.com/SEWSaaS.TS.Reservation/ANTS/api",
        False,
        True,
    )
    aurillac_editor = Editor(
        "aurillac",
        "Aurillac",
        "https://aurillac-grc.e-citiz.com/SEWSaaS.TS.Reservation/ANTS/api",
        False,
        True,
    )
    aubervilliers_editor = Editor(
        "aubervilliers",
        "Aubervilliers",
        "https://ants.saas.smartcjm.com/api",
        False,
        True,
    )
    sens_editor = Editor(
        "sens",
        "Sens",
        "https://rendezvous.ville-sens.fr/api/ants",
        False,
        True,
    )
    mushroom_editor = Editor(
        "mushroom",
        "Mushroom",
        "https://ants.espace-citoyen.fr/api",
        False,
        True,
    )
    iwana_editor = Editor(
        "iwana",
        "Iwana",
        "https://iwana.fr/external-api/ants",
        False,
        True,
    )
    anaximandre_editor = Editor(
        "anaximandre",
        "Anaximandre",
        "https://emgaviou.anaximandre.bzh/api",
        False,
        True,
    )
    dijon_editor = Editor(
        "dijon",
        "Dijon",
        "https://api.metropole-dijon.fr/21231/AntsConnect/v1/api",
        False,
        True,
    )
    quetigny_editor = Editor(
        "quetigny",
        "Quetigny",
        "https://api.metropole-dijon.fr/21515/AntsConnect/v1/api",
        False,
        True,
    )
    condesurlescaut_editor = Editor(
        "condesurlescaut",
        "Condé sur l'escaut",
        "https://www.condesurlescaut.fr/api",
        False,
        True,
    )
    poligny_editor = Editor(
        "poligny",
        "Poligny",
        "https://www.ville-poligny.fr/_rdv/api",
        False,
        True,
    )
    charly_sur_marne_editor = Editor(
        "charlysurmarne",
        "Charly-sur-Marne",
        "https://demarches.charly-sur-marne.fr/api",
        False,
        True,
    )
    montreuil_aux_lions_editor = Editor(
        "montreuilauxlions",
        "Montreuil-aux-Lions",
        "https://demarches.montreuilauxlions.fr/api",
        False,
        True,
    )
    les_mureaux_editor = Editor(
        "lesmureaux",
        "Les Mureaux",
        "https://rdv.lesmureaux.fr/ants-integration/api",
        False,
        True,
    )
    mega_editor = Editor("mega", "Mega", "https://www.mega.com", True, True)
    orionRDV_editor = Editor(
        "orionRDV", "OrionRDV", "https://orionrdv.com/", True, True
    )
    les_mureaux_editor = Editor(
        "lesmureaux",
        "Les Mureaux",
        "https://rdv.lesmureaux.fr/ants-integration/api",
        False,
        True,
    )

    if os.environ.get("MOCK_EDITORS") in ["True", True]:
        return [citopia_editor, mega_editor, orionRDV_editor, synbird_editor]
    else:
        return [
            citopia_editor,
            synbird_editor,
            esii_editor,
            troov_editor,
            rdv_360_editor,
            ypok_editor,
            solocal_editor,
            smartagenda_editor,
            numesia_editor,
            info_local_editor,
            agglocompiegne_editor,
            aggloroyan_editor,
            soultz_editor,
            kembs_editor,
            un23mairie_editor,
            vernalis_editor,
            creasit_editor,
            esii_onpremise_editor,
            agendize_editor,
            anct_editor,
            entrouvert_editor,
            convergence_editor,
            arpege_editor,
            wittisheim_editor,
            pecq_editor,
            lorient_editor,
            neuville_sur_saone_editor,
            mobminder_editor,
            pont_saint_esprit_editor,
            saint_etienne_du_rouvray_editor,
            boisseuil_editor,
            espace_rendez_vous_1_editor,
            espace_rendez_vous_2_editor,
            gallia_editor,
            mourmelon_le_grand_editor,
            meze_editor,
            aiguillon_editor,
            plerin_editor,
            aurillac_editor,
            aubervilliers_editor,
            sens_editor,
            mushroom_editor,
            iwana_editor,
            anaximandre_editor,
            dijon_editor,
            quetigny_editor,
            condesurlescaut_editor,
            poligny_editor,
            charly_sur_marne_editor,
            montreuil_aux_lions_editor,
            les_mureaux_editor,
        ]
