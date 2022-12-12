bulk insert gui_base.dbo.gui_table
from 'F:\output.txt'
    with
    (
	datafiletype = 'widechar',
    fieldterminator = '|',
    rowterminator = '\n'
    );