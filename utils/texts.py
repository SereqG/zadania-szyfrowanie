wikipedia_text = """Maria Salomea Skłodowska-Curie (ur. 7 listopada 1867 w Warszawie, zm. 4 lipca 1934 w Passy) – polsko-francuska uczona w dziedzinach fizyki doświadczalnej i chemii fizycznej, podwójna noblistka – laureatka Nagrody Nobla z fizyki (1903) i chemii (1911).

W 1891 r. wyjechała z Królestwa Polskiego do Paryża, by podjąć studia na Sorbonie (w XIX wieku kobiety nie mogły studiować na ziemiach polskich); następnie pracowała naukowo. Była prekursorką nowej gałęzi chemii – radiochemii. Do jej dokonań należą: rozwinięcie teorii promieniotwórczości, technik rozdzielania izotopów promieniotwórczych oraz odkrycie dwóch nowych pierwiastków – radu i polonu. Z jej inicjatywy prowadzono także badania nad leczeniem raka za pomocą promieniotwórczości."""

text_10 = "KRYPTOGRA"

text_100 = (
    "To jest przykladowy tekst stu znakowy, ktory sluzy do testowania dzialania algorytmow szyfrowania."
)
text_100 = text_100[:100] 

base_sentence = (
    "Algorytmy kryptograficzne odgrywaja kluczowa role w zapewnianiu bezpieczenstwa danych "
    "w systemach informatycznych. "
)
repeat_count = (1000 // len(base_sentence)) + 1
text_1000 = (base_sentence * repeat_count)[:1000]

text_100000 = (base_sentence * ((100000 // len(base_sentence)) + 1))[:100000]

