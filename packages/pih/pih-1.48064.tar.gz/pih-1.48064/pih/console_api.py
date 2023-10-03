from json import tool
from typing import Any, Callable
import importlib.util
import sys
from subprocess import CompletedProcess
from typing import Any
from datetime import datetime, timedelta
import os
import re

pih_exists = importlib.util.find_spec("pih") is not None
if not pih_exists:
    sys.path.append("//pih/facade")
from pih.const import MarkType, PASSWORD, PasswordSettings, CheckableSections, FILE
from pih import PIH, A, ActionValue, ActionStack, Input, Output, Session, while_not_do
from pih.errors import NotFound
from pih.collection import (
    Mark,
    User,
    FullName,
    PersonDivision,
    UserBase,
    LoginPasswordPair,
    MarkGroup,
    Result,
    FieldItemList,
    WorkstationDescription,
    ResourceStatus,
    SiteResourceStatus,
    CTIndicationsValue,
    Workstation,
    RobocopyJobStatus,
    ChillerIndicationsValueContainer,
    PrinterReport,
    DiskStatistics,
    TimeSeriesStatistics,
)
from pih.tools import j, nl, js, b as _b


class ConsoleAppsApi:
    LINE: str = "........................................................"

    def __init__(self, pih: PIH | None = None):
        self.pih = pih or PIH
        self.full_name: FullName | None = None
        self.mark_tab_number: str | None = None
        self.telephone_number: str | None = None
        self.mark_person_division_id: int | None = None
        self.user_is_exists: bool = False
        self.login: str | None = None
        self.password: str | None = None
        self.internal_email: str | None = None
        self.user_container: UserBase
        self.description: str | None = None
        self.use_template_user: bool = False
        self.need_to_create_mark: bool | None = None
        self.yes_no = self.input.yes_no


    def create_qr_code_for_mobile_helper_command(
        self,
        command: str | None = None,
        title: str | None = None,
        show_result: bool = True
    ) -> str | None:
        command = command or self.input.input("Введите название команды")
        title = title or self.input.input("Введите заголовок")
        result: bool = A.A_QR.for_mobile_helper_command(
            command,
            title,
            os.path.join(
                A.PTH.MOBILE_HELPER.QR_CODE_FOLDER,
                A.PTH.replace_prohibited_symbols_from_path_with_symbol(
                    A.PTH.add_extension(command, FILE.EXTENSION.PNG)
                ),
            ),
            56,
        )
        qr_code_image_path: str = A.PTH_QR.mobile_helper_command(command)
        if show_result:
            if result:
                self.output.good(
                    nl(j(
                        (
                            f"Файл qr кода {self.bold(title)} создан.",
                            "Путь к файлу:",
                            self.bold(qr_code_image_path),
                        ),
                        nl()
                    ))
                )
            else:
                self.output.error("qr код не был создан")
        return qr_code_image_path

    def create_qr_code_for_card_registry_folder(
        self, card_registry_folder_name: str | None = None, show_result: bool = True
    ) -> list[str]:
        if A.D_C.empty(card_registry_folder_name):
            card_registry_folder_name = self.input.input(
                f"Введите название папки (или несколько значений названий папок разделенной запятой или пробелом)"
            )
        card_registry_folder_name_list: list[str] = re.split(
            "\W+", card_registry_folder_name
        )
        card_registry_folder_name_list = list(
            map(lambda item: str(item).strip(), card_registry_folder_name_list)
        )
        result_path_list: list[str] = []
        for card_registry_folder_name_item in card_registry_folder_name_list:
            card_registry_folder_name_item = A.D_F.polibase_person_card_registry_folder(
                card_registry_folder_name_item
            )
            result: bool = A.A_QR.for_polibase_person_card_registry_folder(
                card_registry_folder_name_item
            )
            qr_code_image_path: str = (
                PIH.PATH.QR_CODE.polibase_person_card_registry_folder(
                    card_registry_folder_name_item
                )
            )
            if show_result and len(card_registry_folder_name_list) == 1:
                if not result:
                    self.output.error("qr код не был создан")
            if result:
                result_path_list.append(qr_code_image_path)
        return result_path_list

    def disks_information(self, host: str | None = None) -> None:
        host = host or self.input.input(
            "Введите название компьютера или сервера"
        )
        with self.output.make_loading(text="Получение результата..."):
            with self.output.make_indent(2, True):
                if A.C_R.accessibility_by_ping(host):
                    disk_statistics_list: list[DiskStatistics] = list(
                        filter(
                            lambda item: item.size > 0, A.EXC.get_disk_statistics_list(
                                host)
                        )
                    )
                    if A.D_C.empty(disk_statistics_list):
                        self.output.error("Хост не имеет дисков")
                    else:
                        self.output.write_line(nl("Информация о дисках:"))
                        for disk_statistics in disk_statistics_list:
                            self.output.write_line(
                                f"{A.CT_V.BULLET} {self.bold(disk_statistics.name)}: {A.D_F.size(disk_statistics.free_space)} из {A.D_F.size(disk_statistics.size)}"
                            )
                else:
                    self.output.error("Хост не доступен или не найден")

    def resources_and_indications_check(
        self,
        checkable_section_list: list[CheckableSections],
        ask_for_update_before: bool = False,
        force_update: bool = False,
        all: bool = False,
    ) -> None:
        with self.output.make_indent(2):
            if CheckableSections.RESOURCES in checkable_section_list or (
                CheckableSections.WS in checkable_section_list
                or CheckableSections.SERVERS in checkable_section_list
            ):

                def label_function(resource: ResourceStatus, index: int) -> str:
                    result: list[str] = []
                    accessable: bool = resource.accessable
                    status: str = A.D_F.yes_no(accessable, True)
                    result.append(
                        " ".join(
                            (status, self.bold(self.output.blue_str(resource.name)))
                        )
                    )
                    if isinstance(resource, SiteResourceStatus):
                        if resource.check_free_space_status:
                            free_space_result_list: str = (
                                resource.free_space_status.split(" ")
                            )
                            result.append(
                                f"      Cвободное место: {free_space_result_list[0]} ({free_space_result_list[1]})"
                            )
                        if resource.check_certificate_status:
                            result.append(
                                f"      Сертификат доступен до: {resource.certificate_status}"
                            )
                    return A.CT.NEW_LINE.join(result)

                force_update = force_update or (
                    ask_for_update_before
                    and self.yes_no("Обновить перед получением")
                )
                if force_update:
                    self.output.write_line(
                        self.italic(
                            f"{self.get_formatted_given_name()}, ожидайте получение результата..."
                        )
                    )
                for checkable_section in [
                    CheckableSections.RESOURCES,
                    CheckableSections.WS,
                    CheckableSections.SERVERS,
                ]:
                    if checkable_section in checkable_section_list:
                        if self.session.is_mobile:
                            self.output.new_line()
                        if all:
                            self.output.write_line(
                                " ".join(
                                    (
                                        A.CT_V.BULLET,
                                        self.bold(
                                            A.D.check(
                                                checkable_section
                                                == CheckableSections.RESOURCES,
                                                "Основные ресурсы",
                                                A.D.check(
                                                    checkable_section
                                                    == CheckableSections.WS,
                                                    "Наблюдаемые компьютеры",
                                                    "Сервера",
                                                ),
                                            )
                                        ),
                                    )
                                )
                            )
                        with self.output.make_indent(2, True):
                            self.output.write_result(
                                A.R_R.get_status_list(
                                    [checkable_section],
                                    force_update,
                                    all
                                    if len(checkable_section_list) == 1
                                    and CheckableSections.WS in checkable_section_list
                                    else False,
                                ),
                                False,
                                label_function=label_function,
                                separated_result_item=self.session.is_mobile,
                            )
            if CheckableSections.INDICATIONS in checkable_section_list:
                with A.ER.detect():
                    if self.session.is_mobile:
                        self.output.new_line()
                    self.output.write_line(
                        self.bold(f"{A.CT_V.BULLET} Показания в помещении КТ")
                    )
                    with self.output.make_indent(2, True):
                        self.output.write_result(
                            A.R_I.last_ct_value_containers(True))
                        path: str = A.PTH.STATISTICS.get_file_path(
                            A.D.get(A.CT_STATISTICS.Types.CT)
                        )
                        self.output.write_image(
                            self.output.bold("График показаний"),
                            A.D_CO.file_to_base64(path),
                        )
                    self.output.separated_line()
                    self.output.write_line(
                        self.bold(
                            f"{A.CT_V.BULLET} Показания в техническом помещении МРТ"
                        )
                    )
                    chiller_indications_value_container_result: Result[
                        list[ChillerIndicationsValueContainer]
                    ] = A.R_I.last_chiller_value_containers(True)
                    chiller_indications_value_container: ChillerIndicationsValueContainer = A.R.get_first_item(
                        chiller_indications_value_container_result
                    )
                    path: str = A.PTH_I.CHILLER_DATA_IMAGE_LAST
                    modification_timstamp: float = A.PTH.get_modification_time(
                        path)
                    file_creating_datetime: datetime | None = datetime.fromtimestamp(
                        modification_timstamp
                        if modification_timstamp > 0
                        else A.PTH.get_creation_time(path)
                    )
                    with self.output.make_indent(2, True):
                        if A.C_E.has(A.E_B.chiller_was_turned_off()):
                            self.output.write_line(
                                j((A.CT_V.WARNING, "Чиллер выключен!", A.CT_V.WARNING))
                            )
                        else:
                            with self.output.make_indent(2, True):
                                self.output.write_result(
                                    chiller_indications_value_container_result,
                                    title=nl("Показания чиллера")
                                    if A.D_C.INDICATIONS.chiller_value_actual(
                                        chiller_indications_value_container
                                    )
                                    else nl(
                                        j(
                                            (
                                                self.bold("Внимание!"),
                                                ": ",
                                                "Показания чиллера неактуальны",
                                            )
                                        )
                                    ),
                                    separated_result_item=False,
                                )
                                self.output.write_image(
                                    j(
                                        (
                                            nl("Изображение дисплея чиллера"),
                                            "Время снятия:",
                                            A.D_F.datetime(
                                                file_creating_datetime),
                                        )
                                    ),
                                    A.D_CO.file_to_base64(
                                        A.PTH_I.CHILLER_DATA_IMAGE_LAST_RESULT
                                    ),
                                )
                                self.output.write_line(
                                    self.bold(
                                        "Текущая выработка фильтра чиллера МРТ:")
                                )
                                statistics: TimeSeriesStatistics = (
                                    A.D_STAT.for_chiller_filter()
                                )
                                total_seconds: int = (
                                    A.D.now() - statistics.values[-1]
                                ).total_seconds()

                                def repr_value(title: str, value: int) -> str:
                                    return js(
                                        (
                                            "",
                                            A.CT_V.BULLET,
                                            f"{title}:",
                                            self.bold(
                                                js(
                                                    (
                                                        str(
                                                            int(
                                                                100
                                                                * (
                                                                    total_seconds
                                                                    / value
                                                                )
                                                            )
                                                        ),
                                                        "%",
                                                    )
                                                )
                                            ),
                                        )
                                    )

                                self.output.write_line(
                                    j(
                                        (
                                            repr_value(
                                                "Минимальная", statistics.max),
                                            repr_value(
                                                "Средняя", statistics.avg),
                                            repr_value(
                                                "Максимальная", statistics.min),
                                        ),
                                        nl(),
                                    )
                                )
            if CheckableSections.MATERIALIZED_RESOURCES in checkable_section_list:
                if self.session.is_mobile:
                    self.output.new_line()
                self.output.separated_line()
                self.output.write_line(
                    self.bold(js((A.CT_V.BULLET, "Материальные ресурсы")))
                )
                with self.output.make_indent(2, True):
                    for resource_type in A.CT_MR.TYPES:
                        self.output.write_line(
                            js(
                                (
                                    A.CT_V.BULLET,
                                    self.bold(
                                        A.D.get(resource_type).description),
                                )
                            )
                        )
                        with self.output.make_indent(2, True):
                            self.output.write_line(
                                nl(
                                    j(
                                        (
                                            nl(),
                                            self.output.bold("Количество"),
                                            ": ",
                                            str(A.D_MR.get_count(
                                                resource_type)),
                                            " штук",
                                        )
                                    )
                                )
                            )
                            self.output.write_line(
                                A.D_F.statistics(resource_type))
                            self.output.write_image(
                                "График выработки фильтров чиллера МРТ",
                                A.D_CO.file_to_base64(
                                    A.PTH.STATISTICS.get_file_path(
                                        resource_type.name)
                                ),
                            )
            if CheckableSections.VALENTA in checkable_section_list:
                scanned_file_path_list: list[
                    str
                ] = A.PTH.get_file_list_by_directory_info(A.PTH.WS_816_SCAN.VALUE)
                count: int = len(scanned_file_path_list)
                if self.session.is_mobile:
                    self.output.new_line()
                self.output.separated_line()
                self.output.write_line(
                    self.bold(
                        f"{A.CT_V.BULLET} Новые исследования в Валенте: "
                        + ("Нет" if count == 0 else f"Да ({count})")
                    )
                )
                if count > 0:
                    if self.yes_no("Показать отсканированные изображения"):
                        for scanned_file_path in scanned_file_path_list:
                            self.output.write_image(
                                j(
                                    (
                                        "Дата создания файла: ",
                                        A.D_F.datetime(
                                            datetime.fromtimestamp(
                                                A.PTH.get_creation_time(
                                                    scanned_file_path
                                                )
                                            )
                                        ),
                                    )
                                ),
                                A.D_CO.file_to_base64(scanned_file_path),
                            )
                    if self.yes_no("Синхронизировать Валенту"):
                        A.A_ACT.was_done(
                            A.CT_ACT.VALENTA_SYNCHRONIZATION, self.session.user
                        )
            if CheckableSections.PRINTERS in checkable_section_list:

                def printer_report(printer_report: PrinterReport) -> str:
                    report_list: list[str] = []
                    admin_description_list: list[str] = (
                        printer_report.adminDescription or ""
                    ).split(",")
                    name: str = printer_report.ip.split(".")[0]
                    report_list.append(
                        f"{self.bold('Модель')}: {printer_report.model}\n{self.bold('Название')}: {name}\n{self.bold('Описание')}: {printer_report.description}"
                    )
                    if (
                        printer_report.name != -401
                        and "infoless" not in admin_description_list
                    ):
                        for item in (
                            ("Тонер", printer_report.get_toner),
                            None
                            if "drumless" in admin_description_list
                            else ("Драм-юнит", printer_report.get_drum),
                        ):
                            if A.D.is_not_none(item):
                                report_list.append(
                                    f" {A.CT_V.BULLET} {self.bold(item[0])}"
                                )

                                def get_value(
                                    function: Callable[[str], int], color: str
                                ) -> str:
                                    value: int = function(color)
                                    result: str = str(value)
                                    if value < 5:
                                        result += j((" ", A.CT_V.WARNING))
                                    return result

                                report_list += [
                                    f"   {self.bold(color.upper())}: {get_value(item[1], color)}"
                                    for color in (
                                        ["k"]
                                        if "bw" in admin_description_list
                                        else ["c", "m", "y", "k"]
                                    )
                                ]
                    else:
                        report_list.append(
                            f"Принтер {A.D.check(printer_report.accessable, '', 'не ')}доступен"
                        )
                    return j(report_list, nl())

                if self.session.is_mobile:
                    self.output.new_line()
                self.output.separated_line()
                self.output.write_line(
                    self.bold(f"{A.CT_V.BULLET} Отчет по принтерам"))
                printer_report_list: list[PrinterReport] = A.R_PR.report().data
                for printer_report_item in printer_report_list:
                    self.output.separated_line()
                    with self.output.make_indent(2, True):
                        self.output.write_line(
                            printer_report(printer_report_item))
            if not all:
                if CheckableSections.BACKUPS in checkable_section_list:
                    robocopy_job_status_list: Result[
                        list[RobocopyJobStatus]
                    ] = A.R_B.robocopy_job_status_list()
                    sort_by_status: bool = self.yes_no(
                        "Сортировать по статусу",
                        no_label=f"{self.bold(f'Сортировать по дате выполнения - {A.CT_V.NUMBER_SYMBOLS[0]}')}",
                    )
                    A.R.sort(
                        robocopy_job_status_list,
                        (
                            lambda item: item.last_status
                            or max(A.CT_RBK.STATUS_CODE.keys())
                        )
                        if sort_by_status
                        else lambda item: datetime.fromtimestamp(0)
                        if A.D_C.empty(item.last_created)
                        else A.D.datetime_from_string(item.last_created),
                        sort_by_status,
                    )

                    def job_status_item_label_function(
                        job_status: RobocopyJobStatus, index: int
                    ) -> str:
                        name: str = job_status.name
                        source: str = job_status.source
                        destination: str = job_status.destination
                        status: int | None = None
                        date: str | None = None
                        if job_status.active:
                            date = "выполняется"
                        else:
                            if job_status.last_created is not None:
                                date = f"{A.D_F.datetime(job_status.last_created)}"
                            status = job_status.last_status
                        variants: list[str] = [
                            "--" if status is None else self.bold(str(status)),
                            "--" if A.D_C.empty(date) else self.bold(date),
                        ]
                        return j(
                            (
                                f" {A.CT_V.BULLET} ",
                                variants[not sort_by_status],
                                ": ",
                                variants[sort_by_status],
                                j(
                                    (
                                        nl(),
                                        "   ",
                                        name,
                                        ": ",
                                        source,
                                        A.CT_V.ARROW,
                                        destination,
                                    )
                                ),
                            )
                        )

                    variants: list[str] = [
                        self.bold("Статус"),
                        self.bold("Дата выполнения"),
                    ]
                    self.output.write_result(
                        robocopy_job_status_list,
                        False,
                        label_function=job_status_item_label_function,
                        separated_result_item=False,
                        title=j(
                            (
                                f" {A.CT_V.BULLET} ",
                                variants[not sort_by_status],
                                ": ",
                                variants[sort_by_status],
                                nl(),
                                "   Название Robocopy-задания",
                                nl(),
                                ConsoleAppsApi.LINE,
                            )
                        ),
                    )

    def polibase_restart(self) -> None:
        if self.yes_no("Перезапустить сервер Polibase"):
            check_word: str = A.CT_P.NAME
            test: bool = not (
                check_word
                == self.input.input(
                    f"Введите контрольное слово: {self.bold(check_word)}"
                )
            )
            notify: bool = test or self.yes_no(
                "Уведомить пользователей", True)
            title: str = f"Перезапуск Polibase{' test' if test else ''}"
            polibase_host: str = (
                A.CT_H.POLIBASE_TEST.NAME if test else A.CT_H.POLIBASE.NAME
            )
            self.output.write_line(
                A.L.it(
                    f"{title}: Начат процесс закрытия программы Polibase на компьютерах."
                )
            )
            A.A_P.client_program_close_for_all(notify, None, test)
            self.output.new_line()
            self.output.write_line(
                A.L.it(f"{title}: Начат процесс перезагрузки сервера Polibase.")
            )
            A.A_P.restart(test)
            while_not_do(
                lambda: not A.C_R.accessibility_by_ping(polibase_host), sleep_time=5
            )
            self.output.new_line()
            self.output.write_line(
                A.L.it(f"{title}: Начат процесс загрузки сервера Polibase.")
            )
            while_not_do(
                lambda: A.C_R.accessibility_by_ping(polibase_host), sleep_time=5
            )
            self.output.new_line()
            A.E.wait_server_start(polibase_host)
            self.output.write_line(
                A.L.it(f"{title}: Завершен процесс загрузки сервера Polibase.")
            )
            A.ME_P.notify_about_polibase_restarted(test)

    def polibase_client_program_close(
        self, search_value: str | None = None, for_all: bool = False
    ) -> None:
        if for_all:
            check_word: str = A.CT_P.NAME
            test: bool = not (
                check_word
                == (
                    search_value
                    or self.input.input(
                        f"Введите контрольное слово - {self.bold(check_word)}"
                    )
                )
            )
            A.A_P.client_program_close_for_all(
                True,
                self.input.input(
                    "Введите сообщение для пользователей Polibase"),
                test,
            )
        else:
            try:
                workstation_list: Result[list[Workstation]] = A.R_WS.by_any(
                    search_value
                    or self.input.input("Введите запрос для поиска компьютера")
                )

                def every_action(workstation: Workstation) -> None:
                    if A.A_P.client_program_close_for_workstation(workstation):
                        self.output.good(
                            f"Программа Polibase закрыта на компьютере {workstation.name}"
                        )

                A.R.every(workstation_list, every_action)
            except NotFound as error:
                self.output.error(error.get_details())
                search_value = None

    def process_kill(self, host_name: str | None, process_name: str | None) -> None:
        try:
            workstation_list: Result[list[Workstation]] = A.R_WS.by_any(
                host_name or self.input.input(
                    "Введите запрос для поиска компьютера")
            )

            def every_action(workstation: Workstation, process_name: str) -> None:
                process_value: int | str = process_name
                try:
                    process_value = int(process_value)
                except ValueError:
                    pass
                if A.A_WS.kill_process(process_value, workstation.name):
                    self.output.good(
                        A.D.check(
                            isinstance(process_value, str),
                            f'Процесс с именем "{process_value}"',
                            f"Программа с идентификационным номером {process_value}",
                        )
                        + f" закрыта на компьютере {workstation.name}"
                    )
                else:
                    self.output.error("Процесс не найден")

            A.R.every(
                workstation_list,
                lambda workstation: every_action(
                    workstation,
                    process_name
                    or self.input.input("Введите название процесса или его PID"),
                ),
            )
        except NotFound as error:
            self.output.error(error.get_details())
            host_name = None

    @property
    def output(self) -> Output:
        return self.pih.output

    @property
    def input(self) -> Input:
        return self.pih.input

    def send_whatsapp_message(self, telephone_number: str, message: str) -> bool:
        return A.ME_WH_W.send(telephone_number, message, A.CT_ME_WH_W.Profiles.IT)

    def mark_find(self, value: str | None = None) -> None:
        self.output.mark.by_any(value or self.input.mark.any())

    def arg(self, index: int = 0, default_value: Any | None = None) -> Any:
        return self.session.arg(index, default_value)

    def register_ct_indications(self) -> None:
        text: str = f"число, которое может содержать дробную часть разделенную {self.bold('точкой')} или {self.bold('запятой')}"
        number_format_notification_text: str = f"- {self.italic(text)}"

        def float_check_function(
            value: str | None, show_error: bool = True
        ) -> str | None:
            result: float | None = None
            if value is not None:
                result = A.D_Ex.float(value)
            if show_error and result is None:
                self.output.error(
                    f"Введите {self.bold('число')} {number_format_notification_text}"
                )
            return None if result is None else str(result)

        temperature: float = float_check_function(
            self.arg(), False
        ) or self.input.input(
            f"Введите значение {self.bold('температуры')} {number_format_notification_text}",
            check_function=float_check_function,
        )
        humidity: float = float_check_function(self.arg(1), False) or self.input.input(
            f"Введите значение {self.bold('влажности')} {number_format_notification_text}",
            check_function=float_check_function,
        )
        indications_value: CTIndicationsValue = CTIndicationsValue(
            temperature, humidity
        )
        if A.A_I_CT.register(indications_value):
            with self.output.send_to_group(A.CT_ME_WH.GROUP.CT_INDICATIONS):
                self.output.write_result(
                    Result(A.CT_FC.INDICATIONS.CT_VALUE, indications_value),
                    title=f"{self.get_formatted_given_name()}, отправил следующие показания в помещение КТ:",
                )
            self.output.good("Спасибо, показания отправлены")

    def find_free_mark(self, value: str | None = None) -> None:
        self.output.mark.result(
            A.R_M.by_any(value or self.input.mark.any()),
            "Список свободных карт доступа:",
        )

    def find_user(self, value: str | None = None) -> None:
        try:
            result: Result[list[User]] = A.R_U.by_any(
                value or self.input.user.title_any()
            )
        except NotFound as error:
            self.output.error(error.get_details())
        else:
            self.output.user.result(result, "Пользователи:")

    def create_password(self) -> str:
        password: str | None = None
        password_settings: PasswordSettings = PASSWORD.get(
            self.input.indexed_field_list(
                "Выберите тип пароля", A.CT_FC.POLICY.PASSWORD_TYPE
            )
        )
        while True:
            password = self.input.user.generate_password(
                True, password_settings)
            self.output.value("Пароль", password)
            if self.yes_no("Использовать", True):
                break
        if self.yes_no("Отправить в ИТ отдел"):
            A.L.it(f"Сгенерированный пароль:")
            A.L.it(password)
        return password

    def make_mark_as_free(self, value: str | None = None, confirm: bool = True) -> None:
        mark: Mark = self.input.mark.by_any(value)
        mark_type: int = A.D.get(MarkType, mark.type)
        if mark_type == MarkType.FREE:
            self.output.error(
                "Карта доступа с введенным номером уже свободная")
        else:
            if not confirm or self.yes_no("Сделать карту свободной"):
                if mark_type == MarkType.TEMPORARY:
                    temporary_tab_number: int = mark.TabNumber
                    mark = A.R_M.temporary_mark_owner(mark).data
                if A.A_M.make_as_free_by_tab_number(mark.TabNumber):
                    if mark_type == MarkType.TEMPORARY:
                        A.E.it_notify_about_temporary_mark_return(
                            mark, temporary_tab_number
                        )
                    else:
                        A.E.it_notify_about_mark_return(mark)
                    self.output.good(
                        f"Карта доступа с номером {mark.TabNumber} стала свободной"
                    )
                else:
                    self.output.error("Ошибка")
            else:
                self.output.error("Отмена")

    def who_lost_the_mark(self, tab_number: str | None = None):
        try:
            tab_number = tab_number or self.input.tab_number()
            if tab_number is not None:
                try:
                    mark: Mark = A.R_M.by_tab_number(tab_number).data
                    mark_type: MarkType = A.D.get(MarkType, mark.type)
                    if mark_type == MarkType.FREE:
                        self.output.good("Это свободная карта доступа")
                    elif mark_type == MarkType.GUEST:
                        self.output.good("Это гостевая карта доступа")
                    else:
                        if mark_type == MarkType.TEMPORARY:
                            mark = A.R_M.temporary_mark_owner(mark).data
                            tab_number = mark.TabNumber
                            self.output.good("Это временная карта доступа")
                        if mark is not None:
                            telephone_number: str = mark.telephoneNumber
                            self.output.value("Персона", mark.FullName)
                            if not A.C.telephone_number(telephone_number):
                                user: User = A.R_U.by_tab_number(
                                    tab_number).data
                                if user is not None:
                                    telephone_number = user.telephoneNumber
                            if not A.C.telephone_number(telephone_number):
                                self.output.error(f"Телефон не указан")
                            else:
                                self.output.value("Телефон", telephone_number)
                                if self.yes_no("Отправить сообщение", True):
                                    details: str = self.input.input(
                                        f"{self.get_formatted_given_name()}, уточните, где забрать найденную карту"
                                    )
                                    if self.send_whatsapp_message(
                                        telephone_number,
                                        f"День добрый, {A.D.to_given_name(mark.FullName)}, вашу карту доступа ({tab_number}) нашли, заберите ее {details}",
                                    ):
                                        self.output.good(
                                            "Сообщение отправлено")
                                    else:
                                        self.output.error(
                                            "Ошибка при отправке сообщения"
                                        )
                        else:
                            self.output.error("Телефон не указан")
                except NotFound:
                    self.output.error(
                        "Карта доступа, с введенным номером не найдена")
        except KeyboardInterrupt:
            pass

    def bold(self, value: str) -> str:
        return self.output.bold(value)

    def italic(self, value: str) -> str:
        return self.output.italic(value)

    def run_command(self, command: list[str] | None = None) -> None:
        default_host: str = A.OS.host()
        host: str | None = None

        def get_command(value: str | None = None) -> list[str]:
            result: tuple[list[str], list[str]] = A.D.dequotes(
                value or self.pih.input.input("Введите команду")
            )
            return list(
                filter(lambda item: not A.D_C.empty(
                    item), result[0] + result[1])
            )

        command = get_command(
            js(command) if not A.D_C.empty(command) else None)
        use_psexec_executor: bool = A.D_C.empty(
            [
                value
                for value in list(map(lambda item: item.lower(), command))
                if value in A.CT.PSTOOLS.COMMAND_LIST
            ]
        )
        process_result: CompletedProcess | None = None
        if use_psexec_executor:
            if A.D_C.empty(host):
                if self.yes_no(
                    f"Использовать хост {self.bold(default_host)}, для выполнения команды",
                    no_label=f"{self.bold('Или введите название хоста')}",
                ):
                    host = default_host
                else:
                    host = self.input.answer
            while True:
                host = host.lower()
                if A.C_R.accessibility_by_ping(host, count=1):
                    self.output.write_line(
                        nl(f"Команда будет запущена на хосте {self.bold(host)}")
                    )
                    break
                else:
                    self.output.error(f"Хост {self.bold(host)} не доступен")
                    host = self.input.input(
                        "Введите имя хоста, на котором будет выполнена команда"
                    )
            host_is_local: bool = A.OS.host_is_local(host)
        self.output.write_line(
            f"{self.get_formatted_given_name()}, ожидайте окончания выполнения команды..."
        )
        if use_psexec_executor:
            process_result = A.EXC.execute(
                command
                if host_is_local
                else A.EXC.create_command_for_powershell(
                    command, host, interactive=None, run_from_system_account=True
                ),
                True,
                True,
                False,
            )
        else:
            process_result = A.EXC.execute(
                A.EXC.create_command_for_executor(command[0], command[1:]),
                True,
                True,
                False,
            )

        def decode(value: bytes | None) -> str | None:
            if A.D_C.empty(value):
                None
            return value.decode(A.CT_WINDOWS.CHARSETS.ALTERNATIVE)

        output: str = decode(process_result.stdout)
        error: str = decode(process_result.stderr)
        if not A.D_C.empty(output):
            self.output.write_line(output)
        if not A.D_C.empty(error):
            self.output.error()

    def create_new_mark(self):
        self.full_name: str | None = None
        self.mark_tab_number: str | None = None
        self.telephone_number: str | None = None
        self.mark_person_division_id: int | None = None

        def get_full_name() -> ActionValue:
            self.output.header("Заполните ФИО персоны")
            self.full_name = self.input.full_name(True)
            user_exists: bool = not A.C.MARK.exists_by_full_name(
                self.full_name)
            if user_exists:
                self.output.error(
                    "Персона с данной фамилией, именем и отчеством уже есть!"
                )
                if not self.yes_no("Продолжить"):
                    self.session.exit()
            return self.output.get_action_value(
                "ФИО персоны", A.D.fullname_to_string(self.full_name)
            )

        def get_telephone_number() -> ActionValue:
            self.output.header("Заполните номер телефона")
            self.telephone_number = self.input.telephone_number()
            return self.output.get_action_value(
                "Номер телефона", self.telephone_number, False
            )

        def get_tab_number() -> ActionValue:
            self.output.header("Выбор группы и номера для карты доступа")
            free_mark: Mark = self.input.mark.free()
            group_name: str = free_mark.GroupName
            self.mark_tab_number = free_mark.TabNumber
            self.output.value("Группа карты доступа", group_name)
            return self.output.get_action_value("Номер карты пропуска", self.mark_tab_number)

        def get_division() -> ActionValue:
            self.output.header("Выбор подразделения")
            person_division: PersonDivision = self.input.mark.person_division()
            self.mark_person_division_id = person_division.id
            return self.output.get_action_value(
                "Подразделение, к которому прикреплена персона", person_division.name
            )

        ActionStack(
            "Данные пользователя",
            get_full_name,
            get_division,
            get_telephone_number,
            get_tab_number,
            input=self.input,
            output=self.output,
        )
        if self.yes_no("Создать карту доступа для персоны", True):
            if A.A_M.create(
                self.full_name, self.mark_person_division_id, self.mark_tab_number, self.telephone_number
            ):
                self.output.good("Карты доступа создана!")
                A.E.it_notify_about_create_new_mark(self.full_name)
                if self.yes_no("Уведомить персону", True):
                    self.send_whatsapp_message(
                        self.telephone_number,
                        f"Сообщение от ИТ отдела Pacific International Hospital: День добрый, {A.D.to_given_name(self.full_name)}, Вам выдана карта доступа с номером {self.mark_tab_number}",
                    )
            else:
                self.output.error("Карта доступа не создана!")

    def send_workstation_message_to_all(self) -> None:
        message: str = self.input.message(
            f"{self.get_formatted_given_name()}, введите сообщение для всех пользователей"
        )
        A.ME_WS.to_all_workstations(
            message, None, [A.CT_H.WS255], self.session)

    @property
    def user(self) -> User:
        return self.session.user

    @property
    def user_description(self) -> str:
        return A.D_F.description(self.user.description)

    def send_workstation_message(
        self,
        recipient_name: str | None = None,
        message: str | None = None,
        ask_for_use_dialog: bool = True,
    ) -> None:
        recipient: User | WorkstationDescription | None = None
        while True:
            try:
                recipient = A.D.get_first_item(
                    self.input.user.by_any(recipient_name, True)
                )
                if A.D.is_not_none(recipient):
                    break
            except NotFound as error:
                value: str = error.get_value()
                if A.C_WS.name(value):
                    if A.C_WS.exists(value):
                        recipient = A.R_WS.by_name(value).data
                        break
                if recipient is None:
                    recipient_name = None
                    self.output.error(error.get_details())
        if isinstance(recipient, User) and A.R.is_empty(
            A.R_WS.by_login(recipient.samAccountName)
        ):
            self.output.error(
                f"Пользователь {recipient.name} ({recipient.samAccountName}) не залогинен ни за одним компьютером."
            )
        else:
            try:
                use_dialog: bool = False
                if ask_for_use_dialog:
                    use_dialog = A.D_C.empty(message) and self.yes_no(
                        "Начать диалог"
                    )
                else:
                    use_dialog = True
                while True:
                    user_given_name: str = self.get_formatted_given_name(
                        self.user_given_name
                    )
                    if isinstance(recipient, User):
                        message = message or self.input.message(
                            f"{user_given_name}, введите сообщение для пользователя {self.get_formatted_given_name(A.D.to_given_name(recipient))}",
                            f"Сообщение от {self.user_given_name} ({self.user_description}): {A.D.to_given_name(recipient)}, ",
                        )
                        if A.ME_WS.to_user(recipient, message):
                            self.output.good("Сообщение отправлено")
                    else:
                        message = message or self.input.message(
                            f"{user_given_name}, введите сообщение для компьютера {recipient.name}",
                            f"Сообщение от {self.user_given_name} ({self.user_description}): ",
                        )
                        if A.ME_WS.to_workstation(recipient, message):
                            self.output.good("Сообщение отправлено")
                            message = None
                    if use_dialog:
                        self.output.separated_line()
                    else:
                        break
            except KeyboardInterrupt as error:
                if use_dialog:
                    self.output.error("Выход из диалога...")
                else:
                    self.output.error("Отмена...")
                raise error

    @property
    def user_given_name(self) -> str:
        return self.session.user_given_name

    def get_formatted_given_name(self, value: str | None = None) -> str:
        return self.output.user.get_formatted_given_name(value or self.user_given_name)

    def create_temporary_mark(self, owner_mark: Mark | None = None) -> None:
        owner_mark = owner_mark or self.input.mark.by_any()
        mark_group: MarkGroup | None = None
        if self.yes_no("Выдать временную карту доступа из той же группы доступа"):
            mark_group = owner_mark
        temporary_mark: Mark = self.input.mark.free(mark_group)
        self.output.temporary_candidate_for_mark(temporary_mark)
        full_name: str = owner_mark.FullName
        tab_number: str = temporary_mark.TabNumber
        if self.yes_no(
            f"Создать временную карту для {full_name} с табельным номеров {tab_number}",
            True,
        ):
            if A.A_M.make_as_temporary(temporary_mark, owner_mark):
                self.output.good("Временная карта создана")
                telephone_number: str = owner_mark.telephoneNumber
                A.E.it_notify_about_create_temporary_mark(
                    full_name, tab_number)
                if not A.C.telephone_number(telephone_number):
                    user: User = A.R.get_first_item(A.R_U.by_any(owner_mark))
                    if user is not None:
                        telephone_number = user.telephoneNumber
                if A.C.telephone_number(telephone_number):
                    if self.yes_no("Уведомить персону", True):
                        self.send_whatsapp_message(
                            telephone_number,
                            f"Сообщение от ИТ отдела: День добрый, {self.get_formatted_given_name(full_name)}, Вам выдана временная карта доступа с номером {tab_number}",
                        )
            else:
                self.output.error("Ошибка при создании временной карты")
        else:
            self.output.error("Отмена")

    def telephone_number_fix_action(self, user: User) -> None:
        try:
            telephone: str = self.input.telephone_number()
            if A.A_U.set_telephone_number(user, telephone):
                self.output.good("Сохранен")
                self.output.line()
            else:
                self.output.error("Ошибка")
        except KeyboardInterrupt:
            self.output.new_line()
            self.output.error("Отмена")
            self.output.new_line()

    def start_user_telephone_number_editor(self) -> None:
        only_empty_telephone_number_edit: bool = self.yes_no(
            "Редактировать только телефоны, которые не заданы", True
        )
        result: Result[list[User]] = A.R_U.all(True)
        for user in result.data:
            user: User = user
            if A.C_U.user(user):
                if user.telephoneNumber is None:
                    self.output.error(f"{user.name}: нет телефона")
                    self.telephone_number_fix_action(user)
                elif not A.C.telephone_number(user.telephoneNumber):
                    fixed_telephone: str = A.D_F.telephone_number(
                        user.telephoneNumber)
                    if A.C.telephone_number(fixed_telephone):
                        self.output.good(f"{user.name} телефон исправлен")
                        A.A_U.set_telephone_number(user, fixed_telephone)
                    else:
                        self.output.yellow(
                            f"{user.name}: неправильный формат телефона ({user.telephoneNumber})"
                        )
                else:
                    if not only_empty_telephone_number_edit:
                        self.output.good(f"{user.name}: телефон присутствует")
                        self.telephone_number_fix_action(user)
            else:
                self.output.notify(
                    f"{user.name}, похоже не пользователь, у которого должен быть номер телефона"
                )

    def start_user_property_setter(
        self,
        property_name: str,
        search_value: str | None = None,
        choose_user: bool = False,
    ) -> None:
        try:
            user_list: list[User] | None = None
            fields: FieldItemList = A.CT_FC.AD.USER
            active: bool | None = (
                True
                if (
                    property_name == A.CT_UP.PASSWORD
                    or property_name == A.CT_UP.TELEPHONE_NUMBER
                )
                else None
            )
            if choose_user:
                user_list = self.input.user.by_any(search_value, active)
            else:
                result: Result[list[User]] = A.R_U.by_any(
                    self.input.user.title_any(), active
                )
                user_list = result.data
            if property_name == A.CT_UP.USER_STATUS:
                for status in [
                    A.CT_AD.ACTIVE_USERS_CONTAINER_DN,
                    A.CT_AD.INACTIVE_USERS_CONTAINER_DN,
                ]:
                    work_user_list: list[User] = A.D.FILTER.users_by_dn(
                        user_list,
                        A.CT_AD.INACTIVE_USERS_CONTAINER_DN
                        if status == A.CT_AD.ACTIVE_USERS_CONTAINER_DN
                        else A.CT_AD.ACTIVE_USERS_CONTAINER_DN,
                    )
                    for index, user in enumerate(work_user_list):
                        try:
                            self.output.user.result(Result(fields, [user]))
                            if self.yes_no(
                                f"{'Активировать' if status == A.CT_AD.ACTIVE_USERS_CONTAINER_DN else 'Деактивировать' } пользователя"
                            ):
                                if status == A.CT_AD.ACTIVE_USERS_CONTAINER_DN:
                                    if self.yes_no(
                                        "Использовать шаблон для пользователя", True
                                    ):
                                        user_container = self.input.user.template()
                                    else:
                                        user_container = self.input.user.container()
                                else:
                                    user_container = UserBase(
                                        distinguishedName=A.CT_AD.INACTIVE_USERS_CONTAINER_DN
                                    )
                                if A.A_U.set_status(user, status, user_container):
                                    self.output.good("Успешно")
                                else:
                                    self.output.error("Ошибка")
                            else:
                                self.output.new_line()
                                self.output.error("Отмена")
                        except KeyboardInterrupt:
                            self.output.new_line()
                            if index == len(user_list) - 1:
                                self.output.error("Отмена")
                            else:
                                self.output.error("Отмена - следующий")
                            self.output.new_line()
            else:
                for index, user in enumerate(user_list):
                    try:
                        if property_name == A.CT_UP.TELEPHONE_NUMBER:
                            self.output.user.result(
                                Result(fields, [user]), None)
                            telephone = self.input.telephone_number()
                            if A.C.telephone_number(telephone) and self.yes_no(
                                "Установить", True
                            ):
                                if A.A_U.set_telephone_number(user, telephone):
                                    self.output.good("Успешно")
                                else:
                                    self.output.error("Ошибка")
                            else:
                                self.output.error("Отмена")
                        elif property_name == A.CT_UP.PASSWORD:
                            self.output.user.result(
                                Result(fields, [user]), "Пользователи:"
                            )
                            password: str | None = None
                            while True:
                                password = self.input.user.generate_password(
                                    True,
                                    PASSWORD.get(
                                        self.input.indexed_field_list(
                                            "Выберите тип пароля",
                                            A.CT_FC.POLICY.PASSWORD_TYPE,
                                        )
                                    ),
                                )
                                self.output.value("Пароль", password)
                                if self.yes_no("Использовать", True):
                                    break
                            if self.yes_no("Установить", True):
                                if A.A_U.set_password(user, password):
                                    self.output.good("Успешно")
                                else:
                                    self.output.error("Ошибка")
                            else:
                                self.output.error("Отмена")
                    except KeyboardInterrupt:
                        self.output.new_line()
                        self.output.error(
                            "Отмена"
                            + (" - следующий" if index !=
                               len(user_list) - 1 else "")
                        )
                        self.output.new_line()
        except NotFound as error:
            self.output.error(error.get_details())

    @property
    def session(self) -> Session:
        return self.pih.session
    
    def b(self, value: Any) -> str:
        return _b(value) if self.session.is_mobile else str(value)

    def create_new_user(self) -> None:
        self.full_name: FullName | None = None
        self.mark_tab_number: str | None = None
        self.telephone_number: str | None = None
        self.mark_person_division_id: int | None = None
        self.user_is_exists: bool = False
        self.login: str | None = None
        self.password: str | None = None
        self.internal_email: str | None = None
        self.user_container: User | None = None
        self.description: str | None = None
        self.use_template_user: bool | None = None
        self.need_to_create_mark: bool | None = None

        def get_full_name() -> ActionValue:
            self.output.header("Заполнение ФИО пользователя")
            self.full_name = self.input.full_name(True)
            self.user_is_exists = A.C.USER.exists_by_full_name(self.full_name)
            if self.user_is_exists:
                self.output.error(
                    "Пользователем с данной фамилией, именем и отчеством уже есть!"
                )
                if not self.yes_no("Продолжить"):
                    self.session.exit()
            return self.output.get_action_value(
                "ФИО пользователя", A.D.fullname_to_string(self.full_name)
            )

        def get_login() -> ActionValue:
            self.output.header("Создание логина для аккаунта пользователя")
            self.login = self.input.user.generate_login(self.full_name)
            return self.output.get_action_value("Логин пользователя", self.login)

        def get_telephone_number() -> ActionValue:
            self.output.header("Заполнение номера телефона")
            self.telephone_number = self.input.telephone_number()
            return self.output.get_action_value(
                "Номер телефона", self.telephone_number, False
            )

        def get_description() -> ActionValue:
            self.output.header("Заполнение описания пользователя")
            self.description = self.input.description()
            return self.output.get_action_value("Описание", self.description, False)

        def get_template_user_container_or_user_container() -> ActionValue:
            self.output.header("Выбор контейнера для пользователя")
            self.user_container, self.use_template_user = (
                self.input.user.template(),
                True,
            )
            return self.output.get_action_value(
                "Контейнер пользователя", self.user_container.description
            )

        def get_password() -> ActionValue:
            self.output.header("Создание пароля для аккаунта пользователя")
            self.password = self.input.user.generate_password(
                settings=PASSWORD.SETTINGS.PC
            )
            return self.output.get_action_value("Пароль", self.password, False)

        def get_internal_email() -> ActionValue:
            self.internal_email = A.D_F.email(
                self.login, add_default_domain=True)
            return self.output.get_action_value(
                "Адресс корпоративной электронной почты пользователя",
                self.internal_email,
            )
        def get_email_password() -> ActionValue:
            self.email_password = self.password
            return self.output.get_action_value(
                "Пароль электронной почты", self.email_password, False
            ) 

        def get_external_email() -> ActionValue:
            self.output.header("Добавление внешней почты")
            if self.yes_no("Добавить"):
                self.external_email = self.input.email()
            return self.output.get_action_value(
                "Адресс внешней электронной почты пользователя",
                self.external_email if self.external_email else "Нет",
                False,
            )

        def get_mark_person_division() -> ActionValue | None:
            if self.need_to_create_mark and A.D.is_none(self.mark_person_division_id):
                self.output.header("Выбор подразделения")
                mark_person_division: PersonDivision = self.input.mark.person_division(False)
                self.mark_person_division_id = mark_person_division.id
                return self.output.get_action_value(
                    "Подразделение персоны, которой принадлежит карта доступа",
                    mark_person_division.name,
                )
            return None

        def get_tab_number() -> ActionValue:
            full_name_string: str = A.D.fullname_to_string(self.full_name)
            mark: Mark | None = A.R_M.by_name(full_name_string, True).data
            if A.D.is_not_none(mark):
                if self.yes_no(
                    f"Найдена карта доступа для персоны {full_name_string} с номером {mark.TabNumber}. Использовать",
                    True,
                ):
                    self.need_to_create_mark = False
                    self.mark_tab_number = mark.TabNumber
                    self.mark_person_division_id = mark.DivisionID
                    return None
            self.need_to_create_mark = self.yes_no(
                f"Создать карту доступа для персоны '{full_name_string}'", True
            )
            if self.need_to_create_mark:
                self.output.header("Создание карты доступа")
                free_mark: Mark = self.input.mark.free()
                self.mark_tab_number = free_mark.TabNumber
                self.mark_person_division_id = free_mark.DivisionID
                self.output.value("Группа карты доступа", free_mark.GroupName)
                if A.D.is_not_none(free_mark.DivisionID):
                    self.output.value("Подразделение персоны, которой принадлежит карта доступа",
                    free_mark.DivisionName)
                return self.output.get_action_value(
                    "Номер карты доступа", self.mark_tab_number
                )
            return None

        ActionStack(
            "Данные пользователя",
            get_full_name,
            get_login,
            get_password,
            get_telephone_number,
            get_description,
            get_template_user_container_or_user_container,
            get_internal_email,
            get_tab_number,
            get_mark_person_division,
            input=self.input,
            output=self.output,
        )
        full_name_parts: list[str] = list(map(lambda item: item.lower(), self.full_name.as_list()))
        test: bool = "test" in full_name_parts or "тест" in full_name_parts
        if test or self.yes_no("Создать аккаунт для пользователя", True):
            if not test:
                A.A_U.create_from_template(
                    self.user_container.distinguishedName,
                    self.full_name,
                    self.login,
                    self.password,
                    self.description,
                    self.telephone_number,
                    self.internal_email or self.external_email,
                )
                if self.need_to_create_mark:
                    self.mark_tab_number = (
                        self.mark_tab_number
                        or A.R_M.by_name(
                            A.D.fullname_to_string(self.full_name), True
                        ).data.TabNumber
                    )
                    A.A_M.create(
                        self.full_name,
                        self.mark_person_division_id,
                        self.mark_tab_number,
                        self.telephone_number,
                    )
                if A.A_D.create_for_user(
                    A.PTH_U.get_document_name(
                        A.D.fullname_to_string(self.full_name),
                        self.login if self.user_is_exists else None,
                    ),
                    self.full_name,
                    self.mark_tab_number,
                    LoginPasswordPair(self.login, self.password),
                    LoginPasswordPair(self.login, self.password),
                    LoginPasswordPair(self.internal_email, self.password),
                ):
                    A.E.hr_notify_about_new_employee(self.login)
                    A.E.it_notify_about_create_user(self.login, self.password)  
                    self.send_whatsapp_message(
                            self.telephone_number,
                            j((_b("День добрый, ", A.D.to_given_name(self.full_name), ". Мы - отдел информационных технологий ", _b("Pacific International Hospital.")))),
                        )
                    if self.need_to_create_mark:
                        A.E.it_notify_about_create_mark(self.full_name)
                        self.send_whatsapp_message(
                            self.telephone_number,
                            j((_b("Вас ожидает карта доступа с номером ", self.mark_tab_number, self.b(" в отделе кадров")))),
                        )
                    self.send_whatsapp_message(
                        self.telephone_number,
                        j((nl("Данные Вашего аккаунта:"), " ", A.CT_V.BULLET, " Логин: ", nl(self.login), " ", A.CT_V.BULLET, " Пароль: ", nl(self.password), " ", A.CT_V.BULLET, " Электронная почта: ", self.internal_email)),
                    )
            A.A_EM.send(A.CT.TEST.EMAIL_ADDRESS if test else A.R.get_first_item(A.R_U.by_job_position(A.CT_AD.JobPositions.HR)).email, js(("Почта сотрудника", A.D.fullname_to_string(self.full_name))), self.internal_email)