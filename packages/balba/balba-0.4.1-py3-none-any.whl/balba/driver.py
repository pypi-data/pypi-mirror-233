"""Layer that interacts with the kicad-cli executable."""
from subprocess import DEVNULL, STDOUT, CalledProcessError, CompletedProcess, run


class Driver:
    """Component in charge of communicating the application code with the kicad-cli executable."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.output = DEVNULL

        if verbose:
            self.output = STDOUT

    def execute_command(self, *args, **kwargs) -> CompletedProcess:
        """
        Wrapper around `subprocess.run` to execute a command and control its output based on the verbosity levels.
        :param args:
        :param kwargs:
        :return: CompletedProcess, as returned by `subprocess.run`.
        """
        check = kwargs.pop("check", True)
        if not kwargs.get("capture_output"):
            kwargs["stdout"] = self.output

        return run(*args, **kwargs, check=check)

    def version(self) -> str:
        """Version of the available (must be in PATH) kicad-cli executable."""
        try:
            result = self.execute_command(["kicad-cli", "version"], capture_output=True)
            return result.stdout.decode("utf-8").strip()
        except (CalledProcessError, FileNotFoundError):
            return ""

    def export_schematic(self, src: str, dst: str) -> int:
        """
        Export a schematic to a PDF file.
        :param src: path to the schematic
        :param dst: output path (and name)
        :return: return code as provided by kicad-cli
        """
        return self.execute_command(
            ["kicad-cli", "sch", "export", "pdf", "--output", dst, src], check=False
        ).returncode

    def export_board_svg(self, src: str, dst: str, layers: list[str], page_size_mode=2) -> int:
        """
        Export a board to an image file.
        :param src:
        :param dst:
        :param layers:
        :param page_size_mode:
        :return:
        """
        return self.execute_command(
            [
                "kicad-cli",
                "pcb",
                "export",
                "svg",
                f"--page-size-mode={page_size_mode}",
                "--layers",
                ",".join(layers),
                "--output",
                dst,
                src,
            ],
            check=False,
        ).returncode

    def export_python_bom(self, src: str, dst: str) -> int:
        """
        Generate an XML BOM from a KiCad schematic
        :param src: path to the schematic
        :param dst: output path (and name)
        :return:
        """
        return self.execute_command(["kicad-cli", "sch", "export", "python-bom", "--output", dst, src]).returncode
