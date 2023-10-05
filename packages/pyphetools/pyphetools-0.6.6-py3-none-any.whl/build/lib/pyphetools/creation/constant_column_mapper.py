from typing import List
import pandas as pd
from .column_mapper import ColumnMapper
from .hp_term import HpTerm


class ConstantColumnMapper(ColumnMapper):
    def __init__(self, hpo_id=None, hpo_label=None, term_list=None, excluded=False) -> None:
        """Column mapper for cases in all patients have an (optionally excluded)HPO term.

        Args:
            hpo_id (str): HPO  id, e.g., HP:0004321
            hpo_label (str): Corresponding term label
            term_list: list of lists with [label, hpo_id]
            excluded (str): symbol used if the feature was excluded (if None, the feature was observed)
        """
        super().__init__()
        self._hpo_id = hpo_id
        if hpo_id is None and hpo_label is None and term_list is not None:
            self._hpo_terms = []
            for term in term_list:
                if excluded:
                    hpoterm = HpTerm(label=term[0], hpo_id=term[1], observed=False)
                else:
                    hpoterm = HpTerm(label=term[0], hpo_id=term[1], observed=True)
                self._hpo_terms.append(hpoterm)
        elif term_list is None and hpo_id is not None and hpo_label is not None:
            if excluded:
                hpoterm = HpTerm(label=hpo_label, hpo_id=hpo_id, observed=False)
            else:
                hpoterm = HpTerm(label=hpo_label, hpo_id=hpo_id, observed=True)
            self._hpo_terms = [hpoterm]
        else:
            raise ValueError(f"Error: Either hpo_id and hpo_label are not not or a list of HPO terms is passed")
        self._excluded = excluded

    def map_cell(self, cell_contents) -> List[HpTerm]:
        """if this mapper is used, then all individuals in the table have the list of HPO terms

        Args:
            cell_contents (str): not used, can be None or any other value

        Returns:
            List[HpTerm]: list of HPO terms
        """
        return self._hpo_terms

    def preview_column(self, column) -> pd.DataFrame:
        if not isinstance(column, pd.Series):
            raise ValueError("column argument must be pandas Series, but was {type(column)}")
        dlist = []
        for _, value in column.items():
            display = ";".join(hpterm.display_value for hpterm in self._hpo_terms)
            dlist.append(display)
        return pd.DataFrame(dlist)

