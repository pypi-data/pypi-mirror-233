# -*- coding: utf-8 -*-

""" Perform protein grouping """

import re
import pandas as pd


def get_canonical_parsimony_groups(result_df: pd.DataFrame,
                                   contam: bool,
                                   reporters: list,
                                   ) -> pd.DataFrame:
    """
    Perform peptide grouping into protein groups using canonical-priority parsimony.
    This protein grouping algorithm is intended to minimize penalizing the inclusion
    of non-canonical entries in the FASTA which could lead to severel drop in canonical protein identification through
    unique peptides alone . If each protein group has only one gene name, and there is no unique peptide
    for any of the non-canonical proteins, then the group is assumed to represent the canonical protein. This is based
    on the assumption that for most proteins, the canonical protein is likely to have much higher abundance than the
    non-canonical proteins especially when the non-canonical protein has no unique peptide. When the non-canonical
    protein has a unique peptide, the mixed group is not reported. Future work will ratio the intensity of these groups
    based on the unique peptides of canonical and non-canonical proteins. Groups with more than one gene name are
    discarded.
    :param result_df:   Pandas dataframe with protein results to be filtered
    :param contam:      Was the data corrected for contaminants? If so, use the corrected intensities
    :param reporters:   List of reporter names
    :return:            Pandas dataframe with canonical parsimony groups.
                        Will have the same columns as the input dataframe.
                        Each row is a parsimony protein group.
    """

    # Get a subset data frame containing only the distinct protein group values
    distinct_protein_ids = pd.DataFrame({"protein id": result_df['protein id'].unique()})

    def check_non_canonical(string: str) -> bool:
        """
        Check if a string contains the non-canonical hyphenated uniprot accession
        :param string: protein accession string
        :return: bool
        """
        return bool(re.search('-[0-9]+(_H)?\\|', string))

    def return_canonical(string: str) -> str:
        """
        Return the first representative canonical accession
        :param string:  protein group containing accessions separated by commas
        :return:        first canonical accession
        """
        for x in sorted(string.split(',')):
            if not check_non_canonical(x):
                return x
        return string

    distinct_protein_ids['first_canonical'] = pd.Series(map(return_canonical, distinct_protein_ids['protein id']))

    # Get the number of UniProt accessions in each protein group based on the number of commas
    distinct_protein_ids['num_proteins'] = distinct_protein_ids['protein id'].str.count(',') + 1

    def strip_uniprot(string: str) -> str:
        """
        Strip the long Uniprot accession into the short Uniprot ID
        :param string:  UniProt accession (e.g., sp|P12345|ABC1_HUMAN)
        :return:        Short UniProt ID (e.g., P12345)
        """

        un = re.sub("(sp\\|)(.+)(\\|.*$)", "\\2", string)
        return re.sub("-[0-9]+(_H)?$", "", un)

    def get_number_of_gene_names(string: str) -> int:
        """
        Get the number of unique gene names in a protein ID list separated with commas
        :param string:  Protein group UniProt accession list separated with commas
        :return:        Number of unique gene names
        """
        return len(set(map(strip_uniprot, string.split(','))))

    # Get the number of unique gene names in each protein group
    distinct_protein_ids['num_genes'] = pd.Series(map(get_number_of_gene_names, distinct_protein_ids['protein id']))

    # Get a subset list of non-canonical proteins with unique peptides. This list is used to compare
    # against the protein groups to determine if the non-canonical proteins within the group have
    # unique peptides.
    unique_proteins = distinct_protein_ids[distinct_protein_ids['num_proteins'] == 1 ]['protein id']
    unique_noncanonical_proteins = unique_proteins[list(map(check_non_canonical, unique_proteins))]

    def check_non_canonical_has_unique_peptides(string: str) -> bool:
        """
        Check if a protein group contains a non-canonical protein with a unique peptide
        :param string:  Protein group UniProt accession list separated with commas
        :return:        True if the protein group contains a non-canonical protein with a unique peptide
        """
        for x in sorted(string.split(',')):
            if check_non_canonical(x):
                if (unique_noncanonical_proteins.eq(x)).any():
                    return True
        return False

    # Get a list of protein groups that contain a non-canonical protein with a unique peptide
    distinct_protein_ids['overlaps_with_unique_non_canonical'] = \
        pd.Series(map(check_non_canonical_has_unique_peptides, distinct_protein_ids['protein id']))

    # Filter the protein groups to only include those that have only one gene name and do not contain
    # a non-canonical protein with a unique peptide; or those that have only one protein
    filtered_distinct_protein_ids = \
        distinct_protein_ids[ (distinct_protein_ids['num_proteins'] == 1) |
                              ((distinct_protein_ids['overlaps_with_unique_non_canonical'] != True) &
                               (distinct_protein_ids['num_genes'] == 1))]

    # Merge the filtered protein groups with the original protein results

    filtered_protein_df = pd.merge(result_df, filtered_distinct_protein_ids)

    if contam is not None:
        filtered_protein_column_list = ['first_canonical',] + [f'm{reporter}_cor' for reporter in reporters]
    else:
        filtered_protein_column_list = ['first_canonical'] + [f'm{reporter}' for reporter in reporters]

    filtered_protein_df = filtered_protein_df[filtered_protein_column_list]

    # The "first_canonical" column takes the place of the "protein id" column
    filtered_protein_df = filtered_protein_df.rename(columns={'first_canonical': 'protein id'})

    return filtered_protein_df
