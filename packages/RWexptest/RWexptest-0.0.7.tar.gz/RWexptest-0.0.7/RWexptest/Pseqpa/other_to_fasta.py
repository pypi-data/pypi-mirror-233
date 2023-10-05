# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 11:49:04 2023

@author: 22193
"""

import os
import pandas as pd

def excel_csv_to_fasta(input_folder, output_folder, entry_column, sequence_column):
    for filename in os.listdir(input_folder):
        if filename.endswith('.xlsx') or filename.endswith('.csv'):
            # 读取Excel或CSV文件
            if filename.endswith('.xlsx'):
                df = pd.read_excel(os.path.join(input_folder, filename))
            elif filename.endswith('.csv'):
                df = pd.read_csv(os.path.join(input_folder, filename))
            else:
                print("If the file is not in xlsx or csv format, please convert it based on the code.")
                break  # Terminate the loop if file is not .xlsx or .csv

            # 定义输出FASTA文件路径
            fasta_filename = os.path.splitext(filename)[0] + '.fasta'
            fasta_file_path = os.path.join(output_folder, fasta_filename)

            # 转换为 FASTA 格式并保存
            with open(fasta_file_path, 'w') as fasta_file:
                for index, row in df.iterrows():
                    entry = row[entry_column]
                    sequence = row[sequence_column]
                    fasta_file.write(f">{entry}\n{sequence}\n")

# =============================================================================
# # 指定输入和输出文件夹路径以及entry列和sequence列的名称
# input_folder = "D:/Working/Team/Luo_Zeyu/投稿文章/BIB/改稿处理/2_独立测试集同源性划分/output/1_获取sequence数据并转换为fasta格式"
# output_folder = "D:/Working/Team/Luo_Zeyu/投稿文章/BIB/改稿处理/2_独立测试集同源性划分/output/1_获取sequence数据并转换为fasta格式"
# entry_column_name = "Entry"  # 请替换为您的entry列的名称
# sequence_column_name = "Sequence"  # 请替换为您的sequence列的名称
# 
# # 调用函数并传递输入和输出文件夹路径以及列名称
# excel_csv_to_fasta(input_folder, output_folder, entry_column_name, sequence_column_name)
# =============================================================================
