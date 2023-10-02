import base64


def upload_to_crma(sf,in_dataframe,in_dataset_name,in_dateset_label):
    df_bytes = in_dataframe.to_csv(index=False).encode('utf-8')
    df_base64 = base64.b64encode(df_bytes).decode('utf-8')
    res_header = sf.InsightsExternalData.create({
        'Format': 'Csv',
        'EdgemartAlias': in_dataset_name,
        'EdgemartLabel': in_dateset_label,
        'FileName': in_dataset_name,
        'Operation': 'Overwrite',
        'Action': 'None'
    })
    header_id = res_header.get('id')
    res_data = sf.InsightsExternalDataPart.create({
                'DataFile': df_base64,
                'InsightsExternalDataId': header_id,
                'PartNumber': '1'
            })
    res_proc = sf.InsightsExternalData.update(header_id, {
    'Action': 'Process'
        })