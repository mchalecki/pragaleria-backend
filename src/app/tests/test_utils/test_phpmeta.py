from app.api_utils import phpmeta


input1 = (
    'a:5:{s:5:"width";i:1169;s:6:"height";i:1500;'
    's:4:"file";s:27:"2018/06/1529158588942b5.jpg";'
    's:5:"sizes";a:9:{s:9:"thumbnail";a:4:{s:4:"file";'
    's:27:"1529158588942b5-150x150.jpg";s:5:"width";i:150;'
    's:6:"height";i:150;s:9:"mime-type";s:10:"image/jpeg";}'
    's:6:"medium";a:4:{s:4:"file";s:27:"1529158588942b5-234x300.jpg";'
    's:5:"width";i:234;s:6:"height";i:300;s:9:"mime-type";s:10:"image/jpeg";}'
    's:12:"medium_large";a:4:{s:4:"file";s:27:"1529158588942b5-768x985.jpg";'
    's:5:"width";i:768;s:6:"height";i:985;s:9:"mime-type";s:10:"image/jpeg";}'
    's:5:"large";a:4:{s:4:"file";s:28:"1529158588942b5-798x1024.jpg";'
    's:5:"width";i:798;s:6:"height";i:1024;s:9:"mime-type";s:10:"image/jpeg";}'
    's:6:"slider";a:4:{s:4:"file";s:28:"1529158588942b5-1169x914.jpg";'
    's:5:"width";i:1169;s:6:"height";i:914;s:9:"mime-type";s:10:"image/jpeg";}'
    's:9:"big-thumb";a:4:{s:4:"file";s:27:"1529158588942b5-421x540.jpg";'
    's:5:"width";i:421;s:6:"height";i:540;s:9:"mime-type";s:10:"image/jpeg";}'
    's:12:"thumb-square";a:4:{s:4:"file";s:27:"1529158588942b5-421x540.jpg";'
    's:5:"width";i:421;s:6:"height";i:540;s:9:"mime-type";s:10:"image/jpeg";}'
    's:18:"thumb-square-small";a:4:{s:4:"file";s:27:"1529158588942b5-117x150.jpg";'
    's:5:"width";i:117;s:6:"height";i:150;s:9:"mime-type";s:10:"image/jpeg";}'
    's:6:"detail";a:4:{s:4:"file";s:27:"1529158588942b5-150x150.jpg";s:5:"width";'
    'i:150;s:6:"height";i:150;s:9:"mime-type";s:10:"image/jpeg";'
    '}}s:10:"image_meta";a:12:{s:8:"aperture";s:3:"4.5";s:6:"credit";s:0:"";'
    's:6:"camera";s:11:"NIKON D3000";s:7:"caption";s:0:"";s:17:"created_timestamp";'
    's:10:"1529008503";s:9:"copyright";s:0:"";s:12:"focal_length";s:2:"26";'
    's:3:"iso";s:3:"200";s:13:"shutter_speed";s:6:"0.0125";s:5:"title";s:0:"";'
    's:11:"orientation";s:1:"0";s:8:"keywords";a:0:{}}}'
)

output1 = {
   'width': 1169,
   'height': 1500,
   'file':'2018/06/1529158588942b5.jpg',
   'sizes': {
       'thumbnail': {
           'file':'1529158588942b5-150x150.jpg',
           'width': 150,
           'height': 150,
           'mime-type':
           'image/jpeg'
        },
       'medium': {
           'file':'1529158588942b5-234x300.jpg',
           'width': 234,
           'height': 300,
           'mime-type':'image/jpeg'
        },
       'medium_large': {
           'file':'1529158588942b5-768x985.jpg',
           'width': 768,
           'height': 985,
           'mime-type':'image/jpeg'
        },
       'large': {
           'file':'1529158588942b5-798x1024.jpg',
           'width': 798,
           'height': 1024,
           'mime-type':'image/jpeg'
        },
       'slider': {
           'file':'1529158588942b5-1169x914.jpg',
           'width': 1169,
           'height': 914,
           'mime-type':'image/jpeg'
        },
       'big-thumb': {
           'file':'1529158588942b5-421x540.jpg',
           'width': 421,
           'height': 540,
           'mime-type':'image/jpeg'
        },
       'thumb-square': {
           'file':'1529158588942b5-421x540.jpg',
           'width': 421,
           'height': 540,
           'mime-type':'image/jpeg'
        },
       'thumb-square-small': {
           'file':'1529158588942b5-117x150.jpg',
           'width': 117,
           'height': 150,
           'mime-type':'image/jpeg'
        },
       'detail': {
           'file':'1529158588942b5-150x150.jpg',
           'width': 150,
           'height': 150,
           'mime-type':'image/jpeg'
        }
    },
   'image_meta': {
       'aperture':'4.5',
       'credit':'',
       'camera':'NIKON D3000',
       'caption':'',
       'created_timestamp':'1529008503',
       'copyright':'',
       'focal_length':'26',
       'iso':'200',
       'shutter_speed':'0.0125',
       'title':'',
       'orientation':'0',
       'keywords': {}
    }
}


def test_phpmeta_for_thumbnails():
    result = phpmeta.to_dict(input1)
    assert output1 == result


input2 = (
    's:3636:"a:20:{i:1;a:6:{s:2:"id";s:5:"12768";'
    's:10:"katalog_nr";s:1:"1";s:15:"cena_wywolawcza";'
    's:7:"1000.00";s:14:"cena_sprzedazy";s:4:"0.00";'
    's:15:"cena_poaukcyjna";s:0:"";s:9:"sprzedana";s:1:"0";}'
    'i:2;a:6:{s:2:"id";s:5:"12779";s:10:"katalog_nr";s:1:"2";'
    's:15:"cena_wywolawcza";s:6:"900.00";s:14:"cena_sprzedazy";'
    's:4:"0.00";s:15:"cena_poaukcyjna";s:0:"";s:9:"sprzedana";s:1:"0";}'
    'i:3;a:6:{s:2:"id";s:5:"12780";s:10:"katalog_nr";s:1:"3";'
    's:15:"cena_wywolawcza";s:6:"900.00";s:14:"cena_sprzedazy";'
    's:4:"0.00";s:15:"cena_poaukcyjna";s:0:"";s:9:"sprzedana";s:1:"0";}'
    'i:4;a:6:{s:2:"id";s:5:"12781";s:10:"katalog_nr";s:1:"4";'
    's:15:"cena_wywolawcza";s:7:"1200.00";s:14:"cena_sprzedazy";'
    's:4:"0.00";s:15:"cena_poaukcyjna";s:0:"";s:9:"sprzedana";s:1:"0";}'
    'i:5;a:6:{s:2:"id";s:5:"12782";s:10:"katalog_nr";s:1:"5";'
    's:15:"cena_wywolawcza";s:7:"1000.00";s:14:"cena_sprzedazy";'
    's:4:"0.00";s:15:"cena_poaukcyjna";s:0:"";s:9:"sprzedana";s:1:"0";}'
    'i:6;a:6:{s:2:"id";s:5:"12783";s:10:"katalog_nr";s:1:"6";'
    's:15:"cena_wywolawcza";s:6:"800.00";s:14:"cena_sprzedazy";'
    's:4:"0.00";s:15:"cena_poaukcyjna";s:0:"";s:9:"sprzedana";'
    's:1:"1";}i:7;a:6:{s:2:"id";s:5:"12784";s:10:"katalog_nr";'
    's:1:"7";s:15:"cena_wywolawcza";s:6:"800.00";s:14:"cena_sprzedazy";'
    's:4:"0.00";s:15:"cena_poaukcyjna";s:0:"";s:9:"sprzedana";s:1:"0";}'
    'i:8;a:6:{s:2:"id";s:5:"12785";s:10:"katalog_nr";s:1:"8";'
    's:15:"cena_wywolawcza";s:6:"900.00";s:14:"cena_sprzedazy";'
    's:4:"0.00";s:15:"cena_poaukcyjna";s:0:"";s:9:"sprzedana";s:1:"0";}'
    'i:9;a:6:{s:2:"id";s:5:"12786";s:10:"katalog_nr";s:1:"9";'
    's:15:"cena_wywolawcza";s:6:"900.00";s:14:"cena_sprzedazy";'
    's:4:"0.00";s:15:"cena_poaukcyjna";s:0:"";s:9:"sprzedana";s:1:"0";}'
    'i:10;a:6:{s:2:"id";s:5:"12778";s:10:"katalog_nr";s:2:"10";'
    's:15:"cena_wywolawcza";s:6:"900.00";s:14:"cena_sprzedazy";'
    's:4:"0.00";s:15:"cena_poaukcyjna";s:0:"";s:9:"sprzedana";s:1:"0";}'
    'i:11;a:6:{s:2:"id";s:5:"12777";s:10:"katalog_nr";s:2:"11";'
    's:15:"cena_wywolawcza";s:6:"900.00";s:14:"cena_sprzedazy";s:4:"0.00";'
    's:15:"cena_poaukcyjna";s:0:"";s:9:"sprzedana";s:1:"0";}i:12;a:6:{'
    's:2:"id";s:5:"12769";s:10:"katalog_nr";s:2:"12";s:15:"cena_wywolawcza";'
    's:7:"1200.00";s:14:"cena_sprzedazy";s:4:"0.00";s:15:"cena_poaukcyjna";'
    's:0:"";s:9:"sprzedana";s:1:"0";}i:13;a:6:{s:2:"id";s:5:"12770";'
    's:10:"katalog_nr";s:2:"13";s:15:"cena_wywolawcza";s:6:"900.00";'
    's:14:"cena_sprzedazy";s:4:"0.00";s:15:"cena_poaukcyjna";s:0:"";'
    's:9:"sprzedana";s:1:"0";}i:14;a:6:{s:2:"id";s:5:"12771";'
    's:10:"katalog_nr";s:2:"14";s:15:"cena_wywolawcza";s:7:"1100.00";'
    's:14:"cena_sprzedazy";s:4:"0.00";s:15:"cena_poaukcyjna";s:0:"";'
    's:9:"sprzedana";s:1:"0";}i:15;a:6:{s:2:"id";s:5:"12772";'
    's:10:"katalog_nr";s:2:"15";s:15:"cena_wywolawcza";s:7:"1100.00";'
    's:14:"cena_sprzedazy";s:4:"0.00";s:15:"cena_poaukcyjna";s:0:"";'
    's:9:"sprzedana";s:1:"0";}i:16;a:6:{s:2:"id";s:5:"12774";s:10:"katalog_nr";'
    's:2:"16";s:15:"cena_wywolawcza";s:6:"900.00";s:14:"cena_sprzedazy";'
    's:4:"0.00";s:15:"cena_poaukcyjna";s:0:"";s:9:"sprzedana";s:1:"0";}i:17;'
    'a:6:{s:2:"id";s:5:"12773";s:10:"katalog_nr";s:2:"17";s:15:"cena_wywolawcza";'
    's:6:"750.00";s:14:"cena_sprzedazy";s:4:"0.00";s:15:"cena_poaukcyjna";s:0:"";'
    's:9:"sprzedana";s:1:"0";}i:18;a:6:{s:2:"id";s:5:"12775";s:10:"katalog_nr";'
    's:2:"18";s:15:"cena_wywolawcza";s:6:"900.00";s:14:"cena_sprzedazy";s:4:"0.00";'
    's:15:"cena_poaukcyjna";s:0:"";s:9:"sprzedana";s:1:"0";}i:19;a:6:{s:2:"id";'
    's:5:"12776";s:10:"katalog_nr";s:2:"19";s:15:"cena_wywolawcza";s:6:"800.00";'
    's:14:"cena_sprzedazy";s:4:"0.00";s:15:"cena_poaukcyjna";s:0:"";s:9:"sprzedana";'
    's:1:"0";}i:20;a:6:{s:2:"id";s:5:"12787";s:10:"katalog_nr";s:2:"20";'
    's:15:"cena_wywolawcza";s:7:"1000.00";s:14:"cena_sprzedazy";s:4:"0.00";'
    's:15:"cena_poaukcyjna";s:0:"";s:9:"sprzedana";s:1:"0";}}";'
)

output2 = {
    1: {'id':'12768','katalog_nr':'1','cena_wywolawcza':'1000.00','cena_sprzedazy':'0.00','cena_poaukcyjna':'','sprzedana':'0'},
    2: {'id':'12779','katalog_nr':'2','cena_wywolawcza':'900.00','cena_sprzedazy':'0.00','cena_poaukcyjna':'','sprzedana':'0'},
    3: {'id':'12780','katalog_nr':'3','cena_wywolawcza':'900.00','cena_sprzedazy':'0.00','cena_poaukcyjna':'','sprzedana':'0'},
    4: {'id':'12781','katalog_nr':'4','cena_wywolawcza':'1200.00','cena_sprzedazy':'0.00','cena_poaukcyjna':'','sprzedana':'0'},
    5: {'id':'12782','katalog_nr':'5','cena_wywolawcza':'1000.00','cena_sprzedazy':'0.00','cena_poaukcyjna':'','sprzedana':'0'},
    6: {'id':'12783','katalog_nr':'6','cena_wywolawcza':'800.00','cena_sprzedazy':'0.00','cena_poaukcyjna':'','sprzedana':'1'},
    7: {'id':'12784','katalog_nr':'7','cena_wywolawcza':'800.00','cena_sprzedazy':'0.00','cena_poaukcyjna':'','sprzedana':'0'},
    8: {'id':'12785','katalog_nr':'8','cena_wywolawcza':'900.00','cena_sprzedazy':'0.00','cena_poaukcyjna':'','sprzedana':'0'},
    9: {'id':'12786','katalog_nr':'9','cena_wywolawcza':'900.00','cena_sprzedazy':'0.00','cena_poaukcyjna':'','sprzedana':'0'},
    10: {'id':'12778','katalog_nr':'10','cena_wywolawcza':'900.00','cena_sprzedazy':'0.00','cena_poaukcyjna':'','sprzedana':'0'},
    11: {'id':'12777','katalog_nr':'11','cena_wywolawcza':'900.00','cena_sprzedazy':'0.00','cena_poaukcyjna':'','sprzedana':'0'},
    12: {'id':'12769','katalog_nr':'12','cena_wywolawcza':'1200.00','cena_sprzedazy':'0.00','cena_poaukcyjna':'','sprzedana':'0'},
    13: {'id':'12770','katalog_nr':'13','cena_wywolawcza':'900.00','cena_sprzedazy':'0.00','cena_poaukcyjna':'','sprzedana':'0'},
    14: {'id':'12771','katalog_nr':'14','cena_wywolawcza':'1100.00','cena_sprzedazy':'0.00','cena_poaukcyjna':'','sprzedana':'0'},
    15: {'id':'12772','katalog_nr':'15','cena_wywolawcza':'1100.00','cena_sprzedazy':'0.00','cena_poaukcyjna':'','sprzedana':'0'},
    16: {'id':'12774','katalog_nr':'16','cena_wywolawcza':'900.00','cena_sprzedazy':'0.00','cena_poaukcyjna':'','sprzedana':'0'},
    17: {'id':'12773','katalog_nr':'17','cena_wywolawcza':'750.00','cena_sprzedazy':'0.00','cena_poaukcyjna':'','sprzedana':'0'},
    18: {'id':'12775','katalog_nr':'18','cena_wywolawcza':'900.00','cena_sprzedazy':'0.00','cena_poaukcyjna':'','sprzedana':'0'},
    19: {'id':'12776','katalog_nr':'19','cena_wywolawcza':'800.00','cena_sprzedazy':'0.00','cena_poaukcyjna':'','sprzedana':'0'},
    20: {'id':'12787','katalog_nr':'20','cena_wywolawcza':'1000.00','cena_sprzedazy':'0.00','cena_poaukcyjna':'','sprzedana':'0'}
}


def test_phpmeta_for_catalogs():
    result = phpmeta.to_dict(input2)
    assert output2 == result