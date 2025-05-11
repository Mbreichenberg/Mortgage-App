import pandas as pd
import io

def create_excel(schedule, currency_symbol):
    df = pd.DataFrame(schedule)

    # Create formatted versions for viewing, and raw for calculations
    df_display = df.copy()
    df_display['Payment'] = df['Payment'].map(lambda x: f"{currency_symbol}{x:,.2f}")
    df_display['Interest'] = df['Interest'].map(lambda x: f"{currency_symbol}{x:,.2f}")
    df_display['Principal'] = df['Principal'].map(lambda x: f"{currency_symbol}{x:,.2f}")
    df_display['Balance'] = df['Balance'].map(lambda x: f"{currency_symbol}{x:,.2f}")

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_display.to_excel(writer, index=False, sheet_name='AmortizationSchedule')
    output.seek(0)
    return output
