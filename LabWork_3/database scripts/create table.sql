IF OBJECT_ID('dbo.gui_table', 'U') IS NOT NULL
DROP TABLE dbo.gui_table
GO
USE gui_base
-- Create the table in the specified schema
CREATE TABLE gui_table
(
    --пассажир
    id INT NOT NULL PRIMARY KEY, 
    фио [NVARCHAR](200) NOT NULL, 
    дата_рождения [date] NOT NULL, 
    паспорт [NVARCHAR](50) NOT NULL, 
    -- билет
    id_билета [NVARCHAR](50) NOT NULL UNIQUE,
    пункт_отправления [NVARCHAR](50) NOT NULL, 
    пункт_назначения [NVARCHAR](50) NOT NULL, 
    дата_отправления [date] NOT NULL, 
    количество_баллов [NVARCHAR](50) NOT NULL,
    вес_багажа [NVARCHAR](50) NOT NULL,
    -- параметры полета
    время_полета [NVARCHAR](50) NOT NULL, 
    самолет [NVARCHAR](50) NOT NULL
);
GO