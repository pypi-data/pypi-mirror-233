import argparse
import pandas as pd

def rearrange_excel_data(input_filepath, output_filepath, sheet_name="Normalised"):
    normalised_data = pd.read_excel(input_filepath, sheet_name=sheet_name, header=None)

    time_col = pd.Series([i * 10 for i in range(10)], name="Time (min)")

    def process_condition_data(condition_data):
        df = pd.DataFrame(time_col).copy()
        for row_label in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
            df[f'Area ({row_label})'] = None

        area_col = condition_data.iloc[1:, 1].reset_index(drop=True)
        col_idx = 1
        row_idx = 0

        while row_idx < len(area_col) - 10:
            if area_col[row_idx] == "Area":
                row_idx += 1
                values_to_copy = area_col[row_idx:row_idx + 10]
                df.iloc[:, col_idx] = values_to_copy.values
                col_idx += 1
                row_idx += 10
            else:
                row_idx += 1

        return df

    rearranged_data = {}
    for condition in range(1, normalised_data.shape[1], 2):
        if condition in normalised_data.columns and condition + 1 in normalised_data.columns:
            condition_data = normalised_data[[condition, condition + 1]]
            df = process_condition_data(condition_data)
            condition_name = normalised_data[condition][0]
            if pd.notna(condition_name) and isinstance(condition_name, float):
                condition_name = int(condition_name)
            rearranged_data[condition_name] = df

    with pd.ExcelWriter(output_filepath) as writer:
        for condition, df in rearranged_data.items():
            df.to_excel(writer, sheet_name=str(condition), index=False)


def main():
    parser = argparse.ArgumentParser(description='Rearrange FIS data in an Excel file.')
    parser.add_argument('input_filepath', type=str, help='Path to the input Excel file.')
    parser.add_argument('output_filepath', type=str, help='Path where the output Excel file will be saved.')
    parser.add_argument('--sheet_name', type=str, default="Normalised",
                        help='Name of the sheet in the Excel file to process (default: %(default)s).')
    args = parser.parse_args()

    try:
        rearrange_excel_data(args.input_filepath, args.output_filepath, args.sheet_name)
        print(f"Data rearranged successfully. Output saved to {args.output_filepath}.")
    except FileNotFoundError:
        print(f"File not found: {args.input_filepath}")
    except pd.errors.EmptyDataError:
        print(f"No data found in {args.input_filepath}.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
