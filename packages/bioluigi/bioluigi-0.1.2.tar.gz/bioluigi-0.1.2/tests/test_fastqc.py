from bioluigi.tasks import fastqc

def test_generate_report():
    task = fastqc.GenerateReport(
            input_file='SRR6219454_1.fastq.gz',
            output_dir='GSM2831405')

    assert task.output().path == 'GSM2831405/SRR6219454_1_fastqc.html'

