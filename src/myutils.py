'''
實用程式,不太需要隨環境修改的部分都放在這裡
'''
from pathlib import Path
from typing import Dict,List
import csv
from datetime import datetime,timezone

def read_stores(input_file:str,fieldnames:List) -> List[Dict]:
    "以預定的{fieldnames}欄位來讀取csv檔,因此欄位名稱必須與檔案內容第一行一致"
    with open(file = input_file, mode = 'r', encoding = 'utf-8', newline = '') as input:
        csvReader = csv.DictReader(input,fieldnames)
        next(csvReader,None) # skip header row
        results:List[Dict] = []
        for row in csvReader:
            results.append(row)
    return results

def write_csv_report(output_file:str,results: List[Dict]) -> None:
    """將轉換過的資料(results),寫入目標的csv檔(output_file)

    Args:
        results (List[Dict]): 地址轉換的列表
        output_file (str): 儲存的CSV路徑位址
    """
    with open(output_file, mode='w', encoding='utf-8', newline='') as csvfile:
        csvWriter = csv.DictWriter(csvfile,fieldnames=results[0].keys())
        csvWriter.writeheader()
        for result in results:
            csvWriter.writerow(result)
    pass

def create_output_file_name(output_folder:str,input_file_path:str,suffix:str) -> str:
    """組合輸入的csv檔{input_file_path}與輸出的目標資料夾{output_folder},生成新的檔案名稱,並以{suffix}作為副檔名

    Ex:
    ``` python
    s:str = create_output_file_name('Stores.csv','.\output','.html')
    # s = '.\output\[20220419+0000_00'46'17]Stores.html'
    ```

    Args:
        output_folder (str): 預定輸出的資料夾路徑
        input_file_path (str): 輸入的地標檔案路徑(.csv)
        suffix (str): 輸出檔案的附檔名,需附加"."

    Raises:
        ValueError: 輸入的路徑{input_file_path}不是一個檔案
        ValueError: 輸入的路徑{input_file_path}不是'.csv'檔案
        ValueError: 預定輸出的{output_folder}不是一個資料夾

    Returns:
        str: 預定要輸出的檔案名稱,ex:
    """
    input_file_P = Path(input_file_path)
    output_folder_P = Path(output_folder)
    if(not input_file_P.is_file()):
        raise ValueError(f"Input file <{input_file_path}> is not a file.")
    if(not input_file_P.suffix == '.csv'):
        raise ValueError(f'Input file <{input_file_path}> is not a csv file')
    if(not output_folder_P.is_dir()):
        raise ValueError(f'Output folder <{output_folder}> is not a folder.')
    timestamp:str = datetime.strftime(datetime.now(tz=timezone.utc),"[%Y%m%d%z_%H'%M'%S]") # ex: "[20220412+0000_03'55'31]"
    return output_folder_P.joinpath(timestamp + input_file_P.stem).with_suffix(suffix).as_posix()