import streamlit as st
import pandas as pd
import io

# Streamlit app title
st.title("PIM and Item Data Processor")

# File uploader for PIM.xlsx
pim_file = st.file_uploader("Upload PIM.xlsx", type=["xlsx"])

# Initialize df as None
df = None
if pim_file is not None:
    # Read PIM.xlsx
    df = pd.read_excel(pim_file)
    st.success("PIM.xlsx uploaded successfully!")
    
    # File uploader for item.xlsx
    item_file = st.file_uploader("Upload item.xlsx", type=["xlsx"])
    
    if item_file is not None:
        # Read item.xlsx
        req = pd.read_excel(item_file)
        st.success("item.xlsx uploaded successfully!")
        
        # Your original logic
        data = []
        desired = ["catalog-number", "width", "length", "height", "weight", "UPC Code", "origin-country"]

        for i in req['Item No.']:
            result = df[df['catalog-number'] == i][desired]
            mandatory_values = req[req["Item No."] == i][["Item Manufacturers Name", "PIM Catalog Name"]].to_dict(orient='records')

            if result.empty:
                empty_entry = {col: "" for col in desired}
                empty_entry["catalog-number"] = i
                if mandatory_values:
                    empty_entry.update(mandatory_values[0])
                data.append(empty_entry)
            else:
                filtered_data = result.fillna("").to_dict(orient='records')
                for entry in filtered_data:
                    if mandatory_values:
                        entry.update(mandatory_values[0])
                    data.append(entry)

        df_filtered = pd.DataFrame(data, columns=["Item Manufacturers Name", "PIM Catalog Name"] + desired)
        
        # Display the filtered DataFrame
        st.write("### Processed Data")
        st.dataframe(df_filtered)
        
        # Save to CSV and provide download button
        csv_buffer = io.StringIO()
        df_filtered.to_csv(csv_buffer, index=False)
        st.download_button(
            label="Download output.csv",
            data=csv_buffer.getvalue(),
            file_name="output.csv",
            mime="text/csv"
        )
