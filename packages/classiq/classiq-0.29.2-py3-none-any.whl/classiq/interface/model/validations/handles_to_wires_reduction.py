from typing import Dict, Iterable, List, Mapping, Tuple, Type, Union

from classiq.interface.generator.function_params import IOName, PortDirection
from classiq.interface.generator.functions import PortDeclaration
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.generator.quantum_function_call import WireName, WirePair
from classiq.interface.generator.wiring.sliced_wire import InoutSlicedWire
from classiq.interface.helpers.pydantic_model_helpers import Nameable, nameables_to_dict
from classiq.interface.model.handle_binding import HandleBinding, SlicedHandleBinding
from classiq.interface.model.handle_state import (
    Handle,
    HandleState,
    get_unique_handle_names,
)
from classiq.interface.model.local_handle import LocalHandle
from classiq.interface.model.quantum_function_call import QuantumOperation
from classiq.interface.model.validations.port_to_wire_name_generator import (
    PortToWireNameGenerator,
)

_EXPECTED_TERMINAL_STATES: Dict[PortDeclarationDirection, HandleState] = {
    PortDeclarationDirection.Output: HandleState.INITIALIZED,
    PortDeclarationDirection.Inout: HandleState.INITIALIZED,
}


def _initialize_handles_to_state(
    port_declarations: Mapping[IOName, PortDeclaration],
    local_handles: Iterable[LocalHandle],
    name_generator: PortToWireNameGenerator,
) -> Dict[str, Handle]:
    handles_to_state: Dict[str, Handle] = dict()

    for port_decl in port_declarations.values():
        is_input = port_decl.direction.includes_port_direction(PortDirection.Input)
        handles_to_state[port_decl.name] = (
            Handle(wire_name=name_generator.get(port_decl.name))
            if is_input
            else Handle()
        )

    for local_handle in local_handles:
        handles_to_state[local_handle.name] = Handle()

    return handles_to_state


class HandleReducer:
    def __init__(
        self,
        port_declarations: Mapping[IOName, PortDeclaration],
        local_handles: Iterable[LocalHandle],
    ) -> None:
        self._port_declarations = port_declarations.values()
        self._name_generator = PortToWireNameGenerator()
        self._local_handles = local_handles
        self._handles_to_state = _initialize_handles_to_state(
            port_declarations, local_handles, self._name_generator
        )

    @property
    def unconnected_wires(self) -> List[WireName]:
        handle_nameables: List[Nameable] = [
            port_decl
            for port_decl in self._port_declarations
            if port_decl.direction == PortDeclarationDirection.Input
        ]
        handle_nameables += list(self._local_handles)

        return [
            self._handles_to_state[handle.name].wire_name
            for handle in handle_nameables
            if self._handles_to_state[handle.name].state == HandleState.INITIALIZED
        ]

    def _handle_inputs(
        self,
        inputs: Mapping[IOName, HandleBinding],
    ) -> Dict[str, str]:
        wire_inputs: Dict[str, str] = {}
        for port, handle_binding in inputs.items():
            handle_wiring_state = self._handles_to_state[handle_binding.name]

            if handle_wiring_state.state is not HandleState.INITIALIZED:
                handle_wiring_state.append_error(
                    f"Trying to access initialized input handle {handle_binding.name!r} but it is in incorrect state"
                )
                continue

            wire_inputs[port] = handle_wiring_state.wire_name

            handle_wiring_state.uninitialize()

        return wire_inputs

    def _handle_outputs(
        self,
        outputs: Mapping[IOName, HandleBinding],
        handles_to_out_wires: Mapping[str, str],
    ) -> Dict[str, str]:
        wire_outputs = {}
        for port, handle_binding in outputs.items():
            handle_wiring_state = self._handles_to_state[handle_binding.name]

            if handle_wiring_state.state is not HandleState.UNINITIALIZED:
                handle_wiring_state.append_error(
                    f"Trying to access uninitialized output handle {handle_binding.name!r} but it is in incorrect state"
                )
                continue

            wire_outputs[port] = handles_to_out_wires[handle_binding.name]

        return wire_outputs

    def _handle_inouts(
        self,
        inouts: Mapping[IOName, HandleBinding],
        handles_to_out_wires: Mapping[str, str],
    ) -> Dict[str, Union[WirePair, InoutSlicedWire]]:
        wire_inouts: Dict[str, Union[WirePair, InoutSlicedWire]] = {}

        for port, handle_binding in inouts.items():
            handle_wiring_state = self._handles_to_state[handle_binding.name]

            if handle_wiring_state.state is not HandleState.INITIALIZED:
                handle_wiring_state.append_error(
                    f"Trying to access uninitialized inout handle {handle_binding.name!r} but it is in incorrect state"
                )
                continue

            in_wire = handle_wiring_state.wire_name
            out_wire = handles_to_out_wires[handle_binding.name]
            if isinstance(handle_binding, SlicedHandleBinding):
                wire_inouts[port] = InoutSlicedWire(
                    input_name=in_wire,
                    output_name=out_wire,
                    start=handle_binding.start,
                    end=handle_binding.end,
                )
            else:
                wire_inouts[port] = WirePair(in_wire=in_wire, out_wire=out_wire)

        return wire_inouts

    def _advance_state(self, handles_to_out_wires: Mapping[str, str]) -> None:
        for handle_name, out_wire in handles_to_out_wires.items():
            handle_state = self._handles_to_state[handle_name]
            if handle_state.state is not HandleState.ERRORED:
                handle_state.initialize(out_wire)

    def reduce_call(
        self, call: QuantumOperation
    ) -> Tuple[
        Mapping[IOName, WireName],
        Mapping[IOName, WireName],
        Mapping[IOName, Union[WirePair, InoutSlicedWire]],
    ]:
        unique_handles = get_unique_handle_names(
            call.wiring_inouts
        ) | get_unique_handle_names(call.wiring_outputs)
        handles_to_out_wires = {
            handle_name: self._name_generator.get(handle_name)
            for handle_name in unique_handles
        }

        inputs = self._handle_inputs(call.wiring_inputs)
        outputs = self._handle_outputs(call.wiring_outputs, handles_to_out_wires)
        inouts = self._handle_inouts(call.wiring_inouts, handles_to_out_wires)

        self._advance_state(handles_to_out_wires)

        return inputs, outputs, inouts

    def get_input_ports_wiring(self) -> Dict[IOName, WireName]:
        return self._get_current_ports_wiring()

    def get_output_ports_wiring(self) -> Dict[IOName, WireName]:
        return self._get_current_ports_wiring()

    def _get_current_ports_wiring(self) -> Dict[IOName, WireName]:
        return {
            handle_name: state.wire_name
            for handle_name, state in self._handles_to_state.items()
            if handle_name not in nameables_to_dict(list(self._local_handles))
            and state.state is HandleState.INITIALIZED
        }

    def report_errored_handles(self, exception_type: Type[Exception]) -> None:
        self._validate_terminal_handle_state()

        errored_handles = {
            name: state.errors
            for name, state in self._handles_to_state.items()
            if state.state is HandleState.ERRORED
        }
        if errored_handles:
            raise exception_type(
                "\n".join(
                    f"Handle {handle_name!r} was errored with {'. '.join(errors)!r}"
                    for handle_name, errors in errored_handles.items()
                )
            )

    def _validate_terminal_handle_state(self) -> None:
        for port_decl in self._port_declarations:
            handle_state = self._handles_to_state[port_decl.name]
            expected_terminal_state = _EXPECTED_TERMINAL_STATES.get(port_decl.direction)
            if (
                expected_terminal_state is not None
                and handle_state.state is not expected_terminal_state
                and handle_state.state is not HandleState.ERRORED
            ):
                handle_state.append_error(
                    f"At the end of the function, in port {port_decl.name} is expected to be {expected_terminal_state} but it isn't"
                )
