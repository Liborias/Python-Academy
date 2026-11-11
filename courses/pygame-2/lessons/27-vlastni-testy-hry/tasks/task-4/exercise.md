## Testy pauzy, restartu a zavření

Napište testy **model.Hra** a **sestav_sadu()**. Událost vytvoříte přes pygame.event.Event; jako první argument předejte pygame.KEYDOWN a jako pojmenovaný argument key=pygame.K_p. Samotné vytvoření nevyžaduje okno. QUIT nemá parametr key.

Ověřte zastavený čas modelu v pauze, skutečně nový objekt kola a nulové skóre po restartu a bezi=False po QUIT v pauze. AssertIsNot se ptá na identitu objektu, assertEqual na jeho hodnotu. Shodné skóre dvou objektů ještě neznamená, že restart vytvořil nový svět.

Kontrola vyzkouší čas běžící v pauze, opětovné použití starého kola a ignorování zavření. Každá nová sada potřebuje čerstvé objekty hry.
