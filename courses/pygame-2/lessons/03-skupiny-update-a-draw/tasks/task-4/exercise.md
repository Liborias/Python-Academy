### Nová skupina, stejné objekty

`skupina_typu(skupina, typ)` vrátí novou Group se stejnými objekty, pro které platí isinstance(objekt, typ), tedy i jejich potomky. Původní skupina zachová členy, objekty polohy a vzhled. Nová skupina přidá další členství; nejde o kopie herních objektů. Žádná shoda vrátí prázdnou Group. Nevybírejte jen přes `type(objekt) is typ`, to by vynechalo potomky.
