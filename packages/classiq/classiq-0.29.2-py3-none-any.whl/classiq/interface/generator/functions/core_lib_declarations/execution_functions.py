from classiq.interface.generator.functions.classical_function_declaration import (
    ClassicalFunctionDeclaration,
)
from classiq.interface.generator.functions.classical_type import (
    Bool,
    ClassicalList,
    Estimation,
    Histogram,
    Integer,
    IQAERes,
    Real,
    Struct,
    VQEResult,
)
from classiq.interface.generator.functions.quantum_invoker_declaration import (
    QuantumInvokerDeclaration,
)
from classiq.interface.generator.types.builtin_struct_declarations.pauli_struct_declarations import (
    Hamiltonian,
)

SAMPLE_OPERATOR = QuantumInvokerDeclaration(
    name="sample",
    param_decls={},
    return_type=Histogram(),
)

ESTIMATE_OPERATOR = QuantumInvokerDeclaration(
    name="estimate",
    param_decls={
        "hamiltonian": Hamiltonian(),
    },
    return_type=Estimation(),
)

QAE_WITH_QPE_POST_PROCESS_OPERATOR = ClassicalFunctionDeclaration(
    name="qae_with_qpe_result_post_processing",
    param_decls={
        "estimation_register_size": Integer(),
        "estimation_method": Integer(),
        "result": Histogram(),
    },
    return_type=Real(),
)

QSVM_FULL_RUN = QuantumInvokerDeclaration(
    name="qsvm_full_run",
    param_decls={
        "train_data": ClassicalList(element_type=ClassicalList(element_type=Real())),
        "train_labels": ClassicalList(element_type=ClassicalList(element_type=Real())),
        "test_data": ClassicalList(element_type=ClassicalList(element_type=Real())),
        "test_labels": ClassicalList(element_type=ClassicalList(element_type=Real())),
        "predict_data": ClassicalList(element_type=ClassicalList(element_type=Real())),
    },
    return_type=Struct(name="QsvmResult"),
)


VQE_OPERATOR = QuantumInvokerDeclaration(
    name="vqe",
    param_decls={
        "hamiltonian": Hamiltonian(),
        "maximize": Bool(),
        "initial_point": ClassicalList(element_type=Integer()),
        "optimizer_name": Integer(),
        "max_iteration": Integer(),
        "tolerance": Real(),
        "step_size": Real(),
        "skip_compute_variance": Bool(),
        "alpha_cvar": Real(),
    },
    return_type=VQEResult(),
)


IQAE_OPERATOR = QuantumInvokerDeclaration(
    name="iqae",
    param_decls={
        "epsilon": Real(),
        "alpha": Real(),
    },
    return_type=IQAERes(),
)


ClassicalFunctionDeclaration.BUILTIN_FUNCTION_DECLARATIONS.update(
    {
        "sample": SAMPLE_OPERATOR,
        "estimate": ESTIMATE_OPERATOR,
        "qae_with_qpe_result_post_processing": QAE_WITH_QPE_POST_PROCESS_OPERATOR,
        "qsvm_full_run": QSVM_FULL_RUN,
        "vqe": VQE_OPERATOR,
        "iqae": IQAE_OPERATOR,
    }
)
