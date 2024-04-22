CREATE TABLE TaiKhoan
(
	MaTK SERIAL PRIMARY KEY,
	TenDangNhap VARCHAR (50),
	MatKhau VARCHAR (50),
	PhanQuyen  VARCHAR (20) UNIQUE
)

CREATE TABLE Nganh
(
	MaNganh VARCHAR (20) PRIMARY KEY,
	TenNganh VARCHAR (100)
)

CREATE TABLE Lop
(
	MaLop VARCHAR (20) PRIMARY KEY,
	TenLop VARCHAR (100),
	MaNganh VARCHAR (20),
	FOREIGN KEY (MaNganh) REFERENCES Nganh (MaNganh)
)

CREATE TABLE GiangVienHuongDan
(
	MaGV VARCHAR (20) PRIMARY KEY,
	HoTenGV VARCHAR (100),
	NgaySinh DATE,
	SoDienThoai INT,
	MaLop VARCHAR (20),
	PhanQuyen  VARCHAR (20),
	FOREIGN KEY (MaLop) REFERENCES Lop (MaLop),
	FOREIGN KEY (PhanQuyen) REFERENCES TaiKhoan (PhanQuyen)
)

CREATE TABLE SinhVien
(
	MSSV VARCHAR (20) PRIMARY KEY,
	HoTenSV VARCHAR (100),
	NgaySinh DATE,
	SoDienThoai INT,
	MaLop VARCHAR (20),
	PhanQuyen  VARCHAR (20),
	FOREIGN KEY (MaLop) REFERENCES Lop (MaLop),
	FOREIGN KEY (PhanQuyen) REFERENCES TaiKhoan (PhanQuyen)
)

CREATE TABLE PhongGiaoVu
(
	MaPGV VARCHAR (20) PRIMARY KEY,
	TenPhong VARCHAR (100),
	PhanQuyen  VARCHAR (20),
	FOREIGN KEY (PhanQuyen) REFERENCES TaiKhoan (PhanQuyen)
)

CREATE TABLE HocPhan
(
	MaHP VARCHAR (20) PRIMARY KEY,
	TenHP VARCHAR (100),
	SoTinChi INT,
	MaNganh VARCHAR (20),
	FOREIGN KEY (MaNganh) REFERENCES Nganh (MaNganh)
)

CREATE TABLE Diem
(
	MSSV VARCHAR (20),
	MaHP VARCHAR (20),
	DiemGK FLOAT(10),
	DiemCK FLOAT(10),
	PRIMARY KEY (MSSV, MaHP),
	FOREIGN KEY (MSSV) REFERENCES SinhVien (MSSV),
	FOREIGN KEY (MaHP) REFERENCES HocPhan (MaHP)

)
-- Data
INSERT INTO TaiKhoan (TenDangNhap, MatKhau, PhanQuyen) 
VALUES 
    ('admin', '123456@', 'admin'),
    ('GV123', '98765@', 'teacher'),
    ('47.01.104.000', '123123@', 'student')
	
INSERT INTO Nganh (MaNganh, TenNganh)
VALUES 
    ('7480201', N'Công nghệ thông tin'),
    ('7140210', N'Sư Phạm Tin học')

INSERT INTO Lop (MaLop, TenLop, MaNganh)
VALUES 
    ('K47.CNTT', 'K47.CNTT.B', '7480201'),
    ('K47.SPTIN', 'K47.SPTIN.B', '7140210'),
	('K46.CNTT', 'K46.CNTT.A', '7480201'),
    ('K46.SPTIN', 'K46.SPTIN.A', '7140210')

INSERT INTO SinhVien (MSSV, HoTenSV, NgaySinh, SoDienThoai, MaLop, PhanQuyen)
VALUES 
    ('47.01.104.000', N'Nguyễn Văn A', '05-01-2003', 0123456789, 'K47.CNTT', 'student'),
	('46.01.104.000', N'Nguyễn Thị B', '02-15-2002', 0928374824, 'K46.CNTT', 'student')


INSERT INTO PhongGiaoVu (MaPGV, TenPhong, PhanQuyen)
VALUES 
    ('PGV001', N'Phòng Giáo Vụ', 'admin')

INSERT INTO GiangVienHuongDan (MaGV, HoTenGV, NgaySinh, SoDienThoai, MaLop, PhanQuyen)
VALUES 
    ('GV001', 'Nguyễn Văn A', '1990-05-15', 123456789, 'K47.CNTT', 'teacher'),
    ('GV002', 'Trần Thị B', '1985-08-20', 987654321, 'K46.CNTT', 'teacher')

INSERT INTO HocPhan (MaHP, TenHP, SoTinChi, MaNganh)
VALUES 
    ('COMP1401', N'	Phân tích và thiết kế giải thuật', 3, '7480201'),
    ('COMP1069', N'	Công nghệ phần mềm nâng cao', 3, '7480201'),
	('COMP1018', N'	Cơ sở dữ liệu', 3, '7480201'),
    ('COMP1016', N'	Cấu trúc dữ liệu', 3, '7480201'),
    ('PSYC1009', N'Giao tiếp sư phạm', 3, '7140210')

INSERT INTO Diem (MSSV, MaHP, DiemGK, DiemCK)
VALUES 
    ('47.01.104.000', 'COMP1401', 10, 9.0),
    ('47.01.104.000', 'COMP1018', 9.0, 8.0),
    ('46.01.104.000', 'PSYC1009', 7.0, 8.5)

SELECT SinhVien.MSSV, SinhVien.HoTenSV, Diem.MaHP, Diem.DiemGK, Diem.DiemCK
FROM SinhVien
JOIN Diem ON SinhVien.MSSV = Diem.MSSV;

