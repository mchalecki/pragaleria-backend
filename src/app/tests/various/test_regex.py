from app.api_utils.regex_utils import get_dimensions_from_description


def test_normal_painting_strings():
    assert get_dimensions_from_description("akryl, płótno, 100 x 120 cm, sygn. na odwrocie") == [100, 120]
    assert get_dimensions_from_description("olej, płótno, 140 x 40 cm, sygn. na odwrocie") == [140, 40]


def test_3d_strings():
    assert get_dimensions_from_description("patynowane aluminium, 35 x 12 x 9 cm, sygn. na podstawie") == [35, 12,
                                                                                                           9]
    assert get_dimensions_from_description("rzeźba kamienna, 40 x 20 x 6 cm") == [40, 20, 6]


def test_type():
    results1 = get_dimensions_from_description("akryl, płótno, 70 x 60 cm, sygn. l.g. oraz na odwrocie")
    results2 = get_dimensions_from_description("olej, płótno, 49,5 x 72 xm, sygn. p.d.")
    for i in results1 + results2:
        assert isinstance(i, float)


def test_with_other_numbers():
    assert get_dimensions_from_description("mezzotinta, sucha igła, 10/30, 70 x 100 cm, sygn. u dołu") == [70, 100]
    assert get_dimensions_from_description(
        "akwaforta, akwatinta, papier, 51/100, 79 x 79 cm (arkusz), 65 x 65 cm (odcisk płyty); sygnowane, opisane i numerowane na dole (ołówkiem)") == [
               79, 79]


def test_float_3d():
    assert get_dimensions_from_description("patynowane aluminium, 35,62 x 12,33 x 9,123 cm, sygn. na podstawie") == [35.62,
                                                                                                                 12.33,
                                                                                                                 9.123]


def test_float_3d_other_numbers():
    assert get_dimensions_from_description(
        "drewno, żywica epoksydowa, technika własna artysty, ed. 42-100, 7 x 11,5 x 8,5 cm, sygnowana na bocznej ścianie") == [
               7, 11.5, 8.5]
