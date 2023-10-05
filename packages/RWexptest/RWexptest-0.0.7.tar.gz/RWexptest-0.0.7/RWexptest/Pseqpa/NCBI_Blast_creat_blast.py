# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 17:27:14 2023

@author: 22193
"""

from Bio.Blast.Applications import NcbimakeblastdbCommandline
from Bio.Blast.Applications import NcbiblastpCommandline

def create_blast_database(input_fasta_path, output_db_path, dbtype="prot"):
    """
    创建BLAST数据库

    Parameters:
        input_fasta_path (str): 输入的FASTA文件路径。
        output_db_path (str): 输出数据库的路径。
        dbtype (str): 数据库类型，可以是'prot'（蛋白质）或'nucl'（核酸）。

    Returns:
        str: 执行结果消息，成功时返回成功消息，否则返回错误消息。
    """
    try:
        # 创建makeblastdb命令行对象
        makeblastdb_cline = NcbimakeblastdbCommandline(
            input_file=input_fasta_path,
            dbtype=dbtype,
            out=output_db_path
        )

        # 执行makeblastdb命令
        stdout, stderr = makeblastdb_cline()

        # 检查执行结果
        if stderr:
            return f"An error occurred: {stderr}"
        else:
            return "BLAST database created successfully."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# 示例用法
# =============================================================================
# input_fasta_path = "<your_train_data_path/train_data.fasta>"
# output_db_path = "<Blast_database_path/Train_protein_seq_database>"
# dbtype = "prot"  # 蛋白质数据库
# 
# result_message = create_blast_database(input_fasta_path, output_db_path, dbtype)
# =============================================================================


def run_blastp(query_fasta_path, blast_db_path, output_file_path, custom_outfmt):
    """
    执行blastp搜索并保存结果为指定格式的文件

    Parameters:
        query_fasta_path (str): 查询的FASTA文件路径。
        blast_db_path (str): BLAST数据库的路径。
        output_file_path (str): 结果保存的文件路径。
        custom_outfmt (str): 自定义输出格式字符串。

    Returns:
        str: 执行结果消息，成功时返回成功消息，否则返回错误消息。
    """
    try:
        # 创建blastp命令行对象
        blastp_cline = NcbiblastpCommandline(
            query=query_fasta_path,
            db=blast_db_path,
            out=output_file_path,
            outfmt=custom_outfmt  # 设置自定义输出格式
        )

        # 执行blastp搜索
        stdout, stderr = blastp_cline()

        # 检查执行结果
        if stderr:
            return f"An error occurred: {stderr}"
        else:
            return "BLAST search completed successfully."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# 示例用法
# =============================================================================
# query_fasta_path = "<your_test_data_path/test_data.fasta>"
# blast_db_path = "<Blast_database_path/Train_protein_seq_database>"
# output_file_path = "<your_save_path/test_data_blast_results.xml>"
# custom_outfmt = 5  # 自定义输出格式
# 
# result_message = run_blastp(query_fasta_path, blast_db_path, output_file_path, custom_outfmt)
# =============================================================================



