import numpy as np
from itertools import combinations


class GolayCode:
    """
    Code binaire de Golay étendu [24, 12, 8].

    k = 12 : nombre de bits d'information
    n = 24 : longueur du mot de code
    d = 8   : distance minimale
    t = 3   : nombre maximal d'erreurs corrigibles
    """

    def __init__(self):

        self.k = 12
        self.n = 24
        self.d = 8
        self.t = 3

        # Matrices
        self.b_mat = []
        self.generator_mat = []
        self.parity_check = []

        # Table :
        # syndrome de 12 bits -> vecteur d'erreur de 24 bits
        self.syndrome_table = None

    # ============================================================
    # MATRICE B
    # ============================================================

    def b_matrix(self):

        self.b_mat = np.array([
            [1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1],
            [0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
            [1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1],
            [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1],
            [0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1],
            [0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
            [0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1],
            [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
        ], dtype=int)

        return self.b_mat

    # ============================================================
    # MATRICE GENERATRICE G
    # ============================================================

    def generator_matrix(self):

        B = self.b_matrix()

        self.generator_mat = np.zeros(
            (self.n, self.k),
            dtype=int
        )

        # G = [ I ]
        #     [ B ]
        self.generator_mat[:self.k, :] = np.eye(
            self.k,
            dtype=int
        )

        self.generator_mat[self.k:, :] = B

        return self.generator_mat

    # ============================================================
    # MATRICE DE CONTROLE H
    # ============================================================

    def parity_check_matrix(self):

        B = self.b_matrix()

        self.parity_check = np.zeros(
            (self.n, self.k),
            dtype=int
        )

        # H = [ B ]
        #     [ I ]
        self.parity_check[:self.k, :] = B

        self.parity_check[self.k:, :] = np.eye(
            self.k,
            dtype=int
        )

        return self.parity_check

    # ============================================================
    # GETTERS
    # ============================================================

    def get_generator_matrix(self):

        if len(self.generator_mat) == 0:
            self.generator_mat = self.generator_matrix()

        return self.generator_mat

    def get_parity_check_matrix(self):

        if len(self.parity_check) == 0:
            self.parity_check = self.parity_check_matrix()

        return self.parity_check

    def get_b_matrix(self):

        if len(self.b_mat) == 0:
            self.b_mat = self.b_matrix()

        return self.b_mat

    # ============================================================
    # VERIFICATION DES MATRICES
    # ============================================================

    def verify_code(self):

        G = self.get_generator_matrix()
        H = self.get_parity_check_matrix()

        # G^T H = 0 mod 2
        orthogonality = (
            np.matmul(G.T, H) % 2
        )

        orthogonal = np.all(
            orthogonality == 0
        )

        return orthogonal

    # ============================================================
    # ENCODAGE
    # ============================================================

    def encode(self, message):

        message = np.asarray(
            message,
            dtype=int
        )

        if len(message) != self.k:
            raise ValueError(
                f"Le message doit contenir "
                f"{self.k} bits."
            )

        G = self.get_generator_matrix()

        codeword = (
            np.matmul(G, message) % 2
        )

        return codeword.astype(int)

    # ============================================================
    # CALCUL DU SYNDROME
    # ============================================================

    def syndrome(self, received):

        received = np.asarray(
            received,
            dtype=int
        )

        if len(received) != self.n:
            raise ValueError(
                f"Le mot reçu doit contenir "
                f"{self.n} bits."
            )

        H = self.get_parity_check_matrix()

        syndrome = (
            np.matmul(received, H) % 2
        )

        return syndrome.astype(int)

    # ============================================================
    # CONVERSION SYNDROME -> CHAINE
    # ============================================================

    @staticmethod
    def syndrome_to_string(syndrome):

        return "".join(
            str(int(bit))
            for bit in syndrome
        )

    # ============================================================
    # CONSTRUCTION DE LA TABLE DE DECODAGE
    # ============================================================

    def build_syndrome_table(self):

        # Si déjà construite, on la réutilise
        if self.syndrome_table is not None:
            return self.syndrome_table

        H = self.get_parity_check_matrix()

        table = {}

        # --------------------------------------------------------
        # ERREUR DE POIDS 0
        # --------------------------------------------------------

        error = np.zeros(
            self.n,
            dtype=int
        )

        syndrome = (
            np.matmul(error, H) % 2
        )

        key = tuple(
            syndrome.tolist()
        )

        table[key] = error.copy()

        # --------------------------------------------------------
        # ERREURS DE POIDS 1, 2 ET 3
        # --------------------------------------------------------

        for weight in range(
            1,
            self.t + 1
        ):

            for positions in combinations(
                range(self.n),
                weight
            ):

                error = np.zeros(
                    self.n,
                    dtype=int
                )

                error[list(positions)] = 1

                syndrome = (
                    np.matmul(
                        error,
                        H
                    ) % 2
                )

                key = tuple(
                    syndrome.tolist()
                )

                # Pour un code [24,12,8], deux erreurs
                # distinctes de poids <= 3 ne doivent pas
                # avoir le même syndrome.

                if key in table:

                    raise ValueError(
                        "Collision dans la table des "
                        "syndromes.\n"
                        f"Poids de l'erreur : {weight}\n"
                        f"Syndrome : {key}"
                    )

                table[key] = error.copy()

        self.syndrome_table = table

        return self.syndrome_table

    # ============================================================
    # DECODAGE
    # ============================================================

    def decode(self, received):

        received = np.asarray(
            received,
            dtype=int
        )

        if len(received) != self.n:
            raise ValueError(
                f"Le mot reçu doit contenir "
                f"{self.n} bits."
            )

        # --------------------------------------------------------
        # Syndrome
        # --------------------------------------------------------

        syndrome = self.syndrome(
            received
        )

        syndrome_key = tuple(
            syndrome.tolist()
        )

        # --------------------------------------------------------
        # Table
        # --------------------------------------------------------

        table = self.build_syndrome_table()

        # --------------------------------------------------------
        # Syndrome non présent
        #
        # Cela signifie que le motif d'erreur n'est pas
        # représenté parmi les erreurs de poids 0 à 3.
        # --------------------------------------------------------

        if syndrome_key not in table:

            return {
                "success": False,
                "received": received.copy(),
                "corrected": None,
                "error_pattern": None,
                "error_weight": None,
                "syndrome": syndrome.copy()
            }

        # --------------------------------------------------------
        # Motif d'erreur
        # --------------------------------------------------------

        error_pattern = table[
            syndrome_key
        ].copy()

        error_weight = int(
            np.sum(error_pattern)
        )

        # --------------------------------------------------------
        # Correction
        # --------------------------------------------------------

        corrected = np.mod(
            received + error_pattern,
            2
        ).astype(int)

        # --------------------------------------------------------
        # Vérification du mot corrigé
        # --------------------------------------------------------

        corrected_syndrome = (
            self.syndrome(corrected)
        )

        correction_valid = np.all(
            corrected_syndrome == 0
        )

        if not correction_valid:

            raise RuntimeError(
                "Le mot corrigé possède encore "
                "un syndrome non nul."
            )

        return {
            "success": True,
            "received": received.copy(),
            "corrected": corrected,
            "error_pattern": error_pattern,
            "error_weight": error_weight,
            "syndrome": syndrome.copy()
        }
