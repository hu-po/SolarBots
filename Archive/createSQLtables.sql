USE PiBot;
DROP TABLE position;
CREATE TABLE SensorData(SensorType varchar(255), SensorNum int, Reading int, Date DATETIME(6));
# CREATE TABLE SensorData_Smooth(SensorType varchar(255), SensorNum int, Reading int, Date DATETIME(6));
CREATE TABLE Position(Type varchar(255), x float, y float, theta float);
