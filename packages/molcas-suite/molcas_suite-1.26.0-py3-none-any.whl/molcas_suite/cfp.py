import numpy as np
from angmom_suite.basis import extract_blocks, dissect_array, \
    print_sf_term_content, print_so_term_content, sf2ws, sf2ws_amfi, \
    make_angmom_ops_from_mult, unitary_transform
from angmom_suite.crystal import ProjectModelHamiltonian, evaluate_term_space,\
    evaluate_term_operators, print_basis, HARTREE2INVCM
from angmom_suite.utils import plot_op
from .extractor import make_extractor


def make_proj_evaluator(h_file, options):
    return ProjectModelHamiltonianMolcas(h_file, options)


class ProjectModelHamiltonianMolcas(ProjectModelHamiltonian):

    def __init__(self, h_file, options):

        angm = make_extractor(h_file, ("rassi", "SFS_angmom"))[()]
        ener = make_extractor(h_file, ("rassi", "SFS_energies"))[()]
        amfi = make_extractor(h_file, ("rassi", "SFS_AMFIint"))[()]

        spin_mult = make_extractor(h_file, ("rassi", "spin_mult"))[()]

        ops = {
            'sf_angm': list(extract_blocks(angm, spin_mult, spin_mult)),
            'sf_mch': list(map(np.diag, extract_blocks(ener, spin_mult))),
            'sf_amfi': list(map(list, dissect_array(amfi, spin_mult, spin_mult)))
        }

        sf_mult = dict(zip(*np.unique(spin_mult, return_counts=True)))

        self.comp_thresh = options.pop("comp_thresh")
        self.field = options.pop("field")

        super().__init__(ops, sf_mult, **options)

    def __iter__(self):

        if self.model_space is None:
            smult = np.repeat(list(self.sf_mult.keys()), list(self.sf_mult.values()))

            ws_angm = sf2ws(self.ops['sf_angm'], self.sf_mult)
            ws_spin = np.array(make_angmom_ops_from_mult(smult)[0:3])
            ws_hamiltonian = sf2ws(self.ops['sf_mch'], self.sf_mult) + \
                sf2ws_amfi(self.ops['sf_amfi'], self.sf_mult)

            eig, vec = np.linalg.eigh(ws_hamiltonian)
            so_eners = (eig - eig[0]) * HARTREE2INVCM

            sf_eners = [(np.diag(eners) - eners[0, 0]) * HARTREE2INVCM
                        for eners in self.ops['sf_mch']]

            print_sf_term_content(self.ops['sf_angm'], sf_eners, self.sf_mult)
            print_so_term_content(unitary_transform(ws_spin, vec),
                                  unitary_transform(ws_angm, vec),
                                  so_eners, self.sf_mult)

        elif not self.terms:
            term_space, trafo = \
                evaluate_term_space(self.sf_mult, self.model_space,
                                    coupling=self.coupling, complete=True)

            hamiltonian, spin, angm = \
                evaluate_term_operators(
                    self.ops['sf_angm'], self.ops['sf_mch'], self.ops['sf_amfi'],
                    self.sf_mult, term_space, quax=self.quax, complete=True)

            print_basis(trafo(hamiltonian), trafo(spin), trafo(angm),
                        [self.model_space], comp_thresh=self.comp_thresh,
                        field=self.field, plot=self.verbose,
                        S=trafo(spin), L=trafo(angm), J=trafo(spin + angm))

        else:
            yield from super().__iter__()
