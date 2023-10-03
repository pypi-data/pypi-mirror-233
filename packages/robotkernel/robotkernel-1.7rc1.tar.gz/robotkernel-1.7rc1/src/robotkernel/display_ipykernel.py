# -*- coding: utf-8 -*-
from ipykernel.comm import CommManager
from ipykernel.kernelbase import Kernel
from ipykernel.zmqshell import ZMQInteractiveShell
from traitlets import Any
from traitlets import Instance
from traitlets import Type


class DisplayKernel(Kernel):
    """BaseKernel with interactive shell for display hooks."""

    shell = Instance(
        "IPython.core.interactiveshell.InteractiveShellABC", allow_none=True
    )
    shell_class = Type(ZMQInteractiveShell)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Configure IPython shell
        self.shell = self.shell_class.instance(
            parent=self,
            profile_dir=self.profile_dir,
            user_module=self.user_module,
            user_ns=self.user_ns,
            kernel=self,
        )
        self.shell.displayhook.session = self.session
        self.shell.displayhook.pub_socket = self.iopub_socket
        self.shell.displayhook.topic = self._topic("execute_result")
        self.shell.display_pub.session = self.session
        self.shell.display_pub.pub_socket = self.iopub_socket
        self.comm_manager = CommManager(parent=self, kernel=self)
        self.shell.configurables.append(self.comm_manager)

        for type_ in ["comm_open", "comm_msg", "comm_close"]:
            self.shell_handlers[type_] = getattr(self.comm_manager, type_)

    user_module = Any()

    def _user_module_changed(self, name, old, new):
        if self.shell is not None:
            self.shell.user_module = new

    user_ns = Instance(dict, args=(), allow_none=True)

    def _user_ns_changed(self, name, old, new):
        if self.shell is not None:
            self.shell.user_ns = new
            self.shell.init_user_ns()

    def start(self):
        self.shell.exit_now = False
        super().start()

    def set_parent(self, ident, parent, *args, **kwargs):
        """Overridden from parent to tell the display hook and output streams about the parent message."""
        super().set_parent(ident, parent, *args, **kwargs)
        self.shell.set_parent(parent)

    def do_shutdown(self, restart):
        self.shell.exit_now = True

    def send_error(self, content=None):
        self.send_response(self.iopub_socket, "error", content)

    def send_display_data(self, data=None, metadata=None, display_id=None):
        if isinstance(data, str):
            self.send_response(
                self.iopub_socket, "display_data", {"data": {"text/plain": data}}
            )
        else:
            self.send_response(
                self.iopub_socket,
                "display_data",
                {
                    "data": data or {},
                    "metadata": metadata or {},
                    "transient": {"display_id": display_id},
                },
            )

    def send_update_display_data(self, data=None, metadata=None, display_id=None):
        self.send_response(
            self.iopub_socket,
            "update_display_data",
            {
                "data": data or {},
                "metadata": metadata or {},
                "transient": {"display_id": display_id},
            },
        )

    def send_execute_result(self, data=None, metadata=None, display_id=None):
        self.send_response(
            self.iopub_socket,
            "execute_result",
            {
                "data": data or {},
                "metadata": metadata or {},
                "transient": {"display_id": display_id},
                "execution_count": self.execution_count,
            },
        )
