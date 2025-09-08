from src.models import Answer, Question, TimeStampWord
from io import StringIO

### DATA HELPERS

def get_string_from_dataset(df):
        selected_columns = [
            "id", "Coherence", "Lexical", "Grammar",
            "Coherence 3.5-0.1", "Lexical 3.5-0.1", "Grammar 3.5-0.1",
            "Coherence 4-0.8", "Lexical 4-0.8", "Grammar 4-0.8"
        ]
        selected_rows = df.index % 3 == 0
        selected_data = df.loc[selected_rows, selected_columns]
        csv_buffer = StringIO()
        selected_data.to_csv(csv_buffer, index=False)
        return csv_buffer.getvalue()


def get_examples_csv_by_ids(df, selected_examples_ids):
    ids = selected_examples_ids.Examples_ids
    if isinstance(ids, int):
        ids = [ids]
    csv_strings = []
    for id in ids:
        df_transformed = df.loc[df["id"] == id, ["Coherence", "Lexical", "Grammar", "full_transcript"]]
        df_transformed = df_transformed.rename(columns={"full_transcript": "Student's transcript"})
        csv_buffer = StringIO()
        df_transformed.to_csv(csv_buffer, index=False)
        csv_strings.append(csv_buffer.getvalue())
    return csv_strings
