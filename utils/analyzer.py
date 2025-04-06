import pandas as pd

def generate_proposal(row):
    if row['Connectivity Score'] < 40 and row['Literacy Rate'] < 60:
        return f"{row['Village Name']}: Needs urgent intervention in both connectivity and literacy."
    elif row['Connectivity Score'] < 40:
        return f"{row['Village Name']}: Needs improvement in connectivity."
    elif row['Literacy Rate'] < 60:
        return f"{row['Village Name']}: Needs improvement in literacy."
    else:
        return f"{row['Village Name']}: Adequately connected and literate."

def analyze_data(filepath):
    df = pd.read_csv(filepath)
    df['Proposal'] = df.apply(generate_proposal, axis=1)
    proposals = df[['Village Name', 'Proposal']]
    return {
        "proposals": proposals,
        "summary": generate_summary(df.to_dict(orient='records'))  # just in case
    }

def generate_summary(data):
    df = pd.DataFrame(data)
    total_villages = len(df)
    avg_literacy = df['Literacy Rate'].mean()
    avg_connectivity = df['Connectivity Score'].mean()
    weakest_area = df.loc[df['Connectivity Score'].idxmin()]['Village Name']
    
    summary = (
        f"Total villages analyzed: {total_villages}\n"
        f"Average Literacy Rate: {avg_literacy:.2f}%\n"
        f"Average Connectivity Score: {avg_connectivity:.2f}\n"
        f"Area with weakest connectivity: {weakest_area}\n"
    )
    return summary
