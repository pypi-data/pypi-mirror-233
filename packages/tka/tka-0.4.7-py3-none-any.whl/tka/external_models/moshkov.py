import importlib
import os
from typing import List, Union

import chemprop
import numpy as np
import pandas as pd

from tka.utils import (load_l1000_ordered_feature_columns,
                       load_mobc_ordered_feature_columns,
                       prepare_df_for_mobc_predictions,
                       transform_moshkov_outputs)


def load_assay_metadata() -> pd.DataFrame:
    """Loads assay metadata of the assays used by Moshkov et al."""
    with importlib.resources.path("tka.data", "assay_metadata.csv") as file_path:
        return pd.read_csv(file_path)


def predict_from_smiles(smiles_list: List[str], checkpoint_dir: str) -> pd.DataFrame:
    """
    Make predictions from a list of SMILES strings using a trained checkpoint.

    Args:
        smiles_list (List[str]): List of SMILES strings for which to make predictions.
        checkpoint_dir (str): Directory containing the trained checkpoint.

    Returns:
        pd.DataFrame: Predictions with SMILES as indices and assays as columns.

    Examples:
        >>> predict_from_smiles(
        ...     smiles_list=["CCC", "CCCC", "CH4"],
        ...     checkpoint_dir=".../Moshkov(etal)-single-models/2021-02-cp-es-op"
        ... )
        smiles AmyloidFormation.Absorb.AB42_1_1  ... HoxA13DNABinding.FluorOligo.HoxDNA_93_259
        CCC                            0.000082  ...                                  0.442998
        CCCC                           0.000082  ...                                  0.442998
        CH4                      Invalid SMILES  ...                            Invalid SMILES
        (3, 270)
    """
    arguments = [
        "--test_path", "/dev/null",
        "--preds_path", "/dev/null",
        "--checkpoint_dir", checkpoint_dir,
        "--no_features_scaling",
    ]

    args = chemprop.args.PredictArgs().parse_args(arguments)
    preds = chemprop.train.make_predictions(args=args, smiles=smiles_list)

    return transform_moshkov_outputs(
        identifier_col_vals=smiles_list, output=preds, use_full_assay_names=True
    )


def predict_from_mobc(df_real: pd.DataFrame, checkpoint_dir: str) -> pd.DataFrame:
    """
    Make predictions from a dataframe of batch effect corrected morphology profiles from CellProfiler and a trained model checkpoint.

    Args:
        df_real (pd.DataFrame): a pd.DataFrame with the columns being CellProfiler features (1746 features)
            and the index column being the identification column
        checkpoint_dir (str): Directory containing the trained checkpoint.

    Returns:
        pd.DataFrame: Predictions with df_real's first column as indices and assays as columns.

    Examples:

        In the following code, identifier_col remains to the only data left besides CellProfiler features.
        Also, sphering normalization is used to modify df_real and this is why df_dmso is required.

        >>> from tka.utils import prepare_df_for_mobc_predictions
        >>> df_real = pd.read_csv("<path_to_df_real>")
        >>> df_dmso = pd.read_csv("<path_to_df_dmso>")
        >>> out_df = prepare_df_for_mobc_predictions(
        ...     df_dmso=df_dmso, df_real=df_real, identifier_col="Metadata_pert_id"
        ... )
        >>> predict_from_mobsc(
        ...     df_real=out_df,
        ...     checkpoint_dir=".../Moshkov(etal)-single-models/2021-02-mobc-es-op",
        ... )
        smiles         AmyloidFormation.Absorb.AB42_1_1  ...  HoxA13DNABinding.FluorOligo.HoxDNA_93_259
        BRD-K18619710                      0.000000e+00  ...                               0.000000e+00
        BRD-K20742498                      3.456357e-10  ...                               1.632998e-03
                ...                               ...  ...                                        ...
        Shape: (X, 270)
    """
    # Generate and save a dummy smiles CSV file to comply with chemprop_predict
    # Serves no real purpose and does not affect the final predictions in any way
    dummy_smiles = ["CCCC" for _ in range(len(df_real))]
    with open("tmp_smiles.csv", "w") as file:
        for item in ["smiles"] + dummy_smiles:
            file.write(item + "\n")

    # Load the MOBC ordered features to generate .npz file
    mobc_features = load_mobc_ordered_feature_columns()

    # Save the pd.DataFrame so that you can load it from a path
    np.savez("out.npz", features=df_real[mobc_features].to_numpy())

    arguments = [
        "--test_path", "tmp_smiles.csv",
        "--preds_path", "/dev/null",
        "--checkpoint_dir", checkpoint_dir,
        "--features_path", "out.npz",
        "--no_features_scaling",
    ]

    args = chemprop.args.PredictArgs().parse_args(arguments)
    preds = chemprop.train.make_predictions(args=args)

    # Remove temporary files
    os.remove("out.npz")
    os.remove("tmp_smiles.csv")

    return transform_moshkov_outputs(
        identifier_col_vals=list(df_real.index), output=preds, use_full_assay_names=True
    )


def predict_from_ge(df: List[str], gene_id: str, checkpoint_dir: str) -> pd.DataFrame:
    """
    Make predictions from a pd.DataFrame of standard scaled gene expressions and a trained model checkpoint.

    Args:
        df (pd.DataFrame): a pd.DataFrame with the columns being L1000 features (977 features)
            and the index column being the identification column
        checkpoint_dir (str): Directory containing the trained checkpoint.
        gene_id (str): type of identifier present in the header row -
            one of "affyID", "entrezID" or "ensemblID"

    Returns:
        pd.DataFrame: Predictions with df's first column as indices and assays as columns.

    Examples:
        >>> df
            ENSG00000132423  ENSG00000182158  ENSG00000122873  ENSG00000213585  ...
        0         -0.559783         1.127299         0.767661        -0.103637  ...
        1          1.055605        -0.131212         0.170593         0.485176  ...
        ...             ...              ...              ...              ...  ...
        (10, 977)
        # Assuming df is a pd.Dataframe with shape (X, 977)
        # and the columns are either ensembl, entrez or affyIDs.
        >>> predict_from_ge(
        ...     df=df,
        ...     gene_id="ensemblID",
        ...     checkpoint_dir=".../Moshkov(etal)-single-models/2021-02-mobc-es-op"
        ... )
        smiles  AmyloidFormation.Absorb.AB42_1_1  ...  HoxA13DNABinding.FluorOligo.HoxDNA_93_259  ...
        0                               0.013138  ...                                   0.207173  ...
        1                               0.064487  ...                                   0.389113  ...
        ...                                  ...  ...                                        ...  ...
        (10, 270)
    """
    # Generate and save a dummy smiles CSV file to comply with chemprop_predict
    # Serves no real purpose and does not affect the final predictions in any way
    dummy_smiles = ["CCCC" for _ in range(len(df))]
    with open("tmp_smiles.csv", "w") as file:
        for item in ["smiles"] + dummy_smiles:
            file.write(item + "\n")

    valid_gene_ids = ["affyID", "entrezID", "ensemblID"]
    if gene_id not in valid_gene_ids:
        raise ValueError(
            f"Invalid gene_id argument -> ({gene_id}). Should be one of {valid_gene_ids}."
        )

    # Load the MOBC ordered features to generate .npz file
    l1000_features = load_l1000_ordered_feature_columns(gene_id)

    # Save the pd.DataFrame so that you can load it from a path
    np.savez("out.npz", features=df[l1000_features].to_numpy())

    arguments = [
        "--test_path", "tmp_smiles.csv",
        "--preds_path", "/dev/null",
        "--checkpoint_dir", checkpoint_dir,
        "--features_path", "out.npz",
        "--no_features_scaling",
    ]

    args = chemprop.args.PredictArgs().parse_args(arguments)
    preds = chemprop.train.make_predictions(args=args)

    # Remove temporary files
    os.remove("out.npz")
    os.remove("tmp_smiles.csv")

    return transform_moshkov_outputs(
        identifier_col_vals=list(df.index), output=preds, use_full_assay_names=True
    )


if __name__ == "__main__":
    # predict_from_smiles(
    #     smiles_list=["CCC"],
    #     checkpoint_dir="/home/filip/Downloads/Moshkov(etal)-single-models/2021-02-cp-es-op"
    # )
    common_path = "/home/filip/Documents/TKA/2023_Moshkov_NatComm/analysis/"
    df_real = pd.read_csv(common_path + "real.csv")
    df_real = df_real.iloc[:10, :]
    df_dmso = pd.read_csv(common_path + "dmso.csv")
    out_df = prepare_df_for_mobc_predictions(
        df_dmso=df_dmso, df_real=df_real, identifier_col="Metadata_pert_id"
    )
    out = predict_from_mobc(
        df_real=out_df,
        checkpoint_dir="/home/filip/Downloads/Moshkov(etal)-single-models/2021-02-mobc-es-op",
    )
    print(out)
