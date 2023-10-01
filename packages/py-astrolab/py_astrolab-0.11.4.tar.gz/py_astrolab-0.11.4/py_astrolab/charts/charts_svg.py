#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# * TODO: Change the label for language in 2 objects, one for IT and one for ENG.
# * Then change the label for planets like this: planet["label"] => planet[language]

import math
from datetime import datetime
from pathlib import Path
from string import Template
from typing import Union

import pytz

from py_astrolab.aspects import CompositeAspects, NatalAspects
from py_astrolab.main import KrInstance
from py_astrolab.types import ChartType, KerykeionException

# calculation and svg drawing class


class MakeSvgInstance:
    """
    Creates the instance that can genearte the chart with the
    function makeSVG().

    There are 2 templates, the extended (default) which has all the
    information and the basic, which has just the chart.

    Parameters:
        - first_obj: First kerykeion object
        - chart_type: Natal, Transit, Composite (Default: Type="Natal")
        - second_obj: Second kerykeion object (Not required if type is Natal)
        - new_output_directory: Set the output directory (default: output_directory)
        - template_type: set the template type to include or not the aspects grid, default: extended)
        - lang: language settings (default: "EN")
        - settings: Set the settings
    """

    def __init__(
            self,
            first_obj: KrInstance,
            chart_type: ChartType = "Natal",
            second_obj: Union[KrInstance, None] = None,
            new_output_directory: Union[str, None] = None,
            template_type: str = "extended",
            lang: str = "EN",
            settings: Union[str, Path, None] = None
    ):

        # Directories:
        DATADIR = Path(__file__).parent
        self.homedir = Path.home()

        if new_output_directory:
            self.output_directory = Path(new_output_directory)
        else:
            self.output_directory = self.homedir

        # Template types:
        if template_type == "basic":
            self.xml_svg = DATADIR / 'templates/basic.xml'
        elif template_type == 'minimal':
            self.xml_svg = DATADIR / 'templates/minimal.xml'
        else:
            self.xml_svg = DATADIR / 'templates/extended.xml'

        # SVG Width
        self.natal_width = 772.2
        self.full_width = 1200

        # Settings file:
        self.settings = settings
        self.language_settings = settings['language_settings'].get(
            lang, "EN")
        self.colors_settings = settings['colors']
        self.planets_settings = settings['planets']
        self.axes_settings = settings['axes']
        self.aspects_settings = settings['aspects']
        self.chart_type = chart_type

        # Kerykeion instance
        self.user = first_obj
        if not hasattr(self.user, "sun"):
            print(f"Generating kerykeion object for {self.user.name}...")
            self.user.__get_all()

        # Make a list for the absolute degrees of the points of the graphic.

        self.points_deg_ut = self.user.planets_degrees + [self.user.houses_degree_ut[0],
                                                          self.user.houses_degree_ut[9], self.user.houses_degree_ut[6],
                                                          self.user.houses_degree_ut[3]]

        # Make a list of the relative degrees of the points in the graphic.

        self.points_deg = []
        for planet in self.user.planets_list:
            self.points_deg.append(planet["position"])

        self.points_deg = self.points_deg + [
            self.user.houses_list[0]["position"],
            self.user.houses_list[9]["position"],
            self.user.houses_list[6]["position"],
            self.user.houses_list[3]["position"]
        ]

        # Make list of the poits sign.

        self.points_sign = []

        for planet in self.user.planets_list:
            self.points_sign.append(planet["sign_num"])

        self.points_sign = self.points_sign + [
            self.user.axis_list[0]["sign_num"],
            self.user.axis_list[1]["sign_num"],
            self.user.axis_list[2]["sign_num"],
            self.user.axis_list[3]["sign_num"]
        ]
        # Make a list of poits if they are retrograde or not.

        self.points_retrograde = []

        for planet in self.user.planets_list:
            self.points_retrograde.append(planet["retrograde"])
        self.points_retrograde = self.points_retrograde + [
            False,
            False,
            False,
            False
        ]

        # Makes the sign number list.

        self.houses_sign_graph = []
        for h in self.user.houses_list:
            self.houses_sign_graph.append(h['sign_num'])

        if self.chart_type == "Natal":
            natal_aspects_instance = NatalAspects(
                self.user, settings=self.settings)
            self.aspects_list = natal_aspects_instance.get_relevant_aspects()

        if (self.chart_type == "Transit" or self.chart_type == "Composite"):  # TODO: If not second should exit

            if not second_obj:
                raise KerykeionException(
                    "Second object is required for Transit or Composite charts.")

            # Kerykeion instance
            self.t_user = second_obj

            if not hasattr(self.t_user, "sun"):
                print(f"Generating kerykeion object for {self.t_user.name}...")
                self.t_user.__get_all()

            # Make a list for the absolute degrees of the points of the graphic.

            self.t_points_deg_ut = self.t_user.planets_degrees
            # Make a list of the relative degrees of the points in the graphic.

            self.t_points_deg = []
            for planet in self.t_user.planets_list:
                self.t_points_deg.append(planet["position"])

            self.t_points_deg = self.t_points_deg

            # Make list of the poits sign.

            self.t_points_sign = []

            for planet in self.t_user.planets_list:
                self.t_points_sign.append(planet["sign_num"])

            self.t_points_sign = self.t_points_sign

            # Make a list of poits if they are retrograde or not.

            self.t_points_retrograde = []

            for planet in self.t_user.planets_list:
                self.t_points_retrograde.append(planet["retrograde"])

            self.t_points_retrograde = self.t_points_retrograde

            self.t_houses_sign_graph = []
            for h in self.t_user.houses_list:
                self.t_houses_sign_graph.append(h['sign_num'])

        # screen size
        if self.chart_type == "Natal":
            self.screen_width = 772.2
        else:
            self.screen_width = 1200
        self.screen_height = 772.2

        # check for home
        self.home_location = self.user.city
        self.home_geolat = self.user.lat
        self.home_geolon = self.user.lng
        self.home_countrycode = self.user.nation
        self.home_timezonestr = self.user.tz_str

        print(f'{self.user.name} birth location: {self.home_location}, {self.home_geolat}, {self.home_geolon}')

        # default location
        self.location = self.home_location
        self.geolat = float(self.home_geolat)
        self.geolon = float(self.home_geolon)
        self.countrycode = self.home_countrycode
        self.timezonestr = self.home_timezonestr

        # current datetime
        now = datetime.now()

        # aware datetime object
        dt_input = datetime(
            now.year, now.month, now.day, now.hour, now.minute, now.second)
        dt = pytz.timezone(self.timezonestr).localize(dt_input)

        # naive utc datetime object
        dt_utc = dt.replace(tzinfo=None) - dt.utcoffset()

        # Default
        self.name = self.user.name
        self.charttype = self.chart_type
        self.year = self.user.utc.year
        self.month = self.user.utc.month
        self.day = self.user.utc.day
        self.hour = self.user.utc.hour + self.user.utc.minute/100
        self.timezone = self.__offsetToTz(dt.utcoffset())
        self.altitude = 25
        self.geonameid = None

        # Transit

        if self.chart_type == "Transit":
            self.t_geolon = self.geolon
            self.t_geolat = self.geolat
            self.t_altitude = self.altitude
            self.t_name = self.language_settings['transit_name']
            self.t_year = dt_utc.year
            self.t_month = dt_utc.month
            self.t_day = dt_utc.day
            self.t_hour = self.__decHourJoin(
                dt_utc.hour, dt_utc.minute, dt_utc.second)
            self.t_timezone = self.__offsetToTz(dt.utcoffset())
            self.t_altitude = 25
            self.t_geonameid = None

        # configuration
        # ZOOM 1 = 100%
        self.zoom = 1

        # 12 zodiacs
        self.zodiac = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo',
                       'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']
        self.zodiac_short = ['Ari', 'Tau', 'Gem', 'Cnc', 'Leo',
                             'Vir', 'Lib', 'Sco', 'Sgr', 'Cap', 'Aqr', 'Psc']
        self.zodiac_color = ['#482900', '#6b3d00', '#5995e7', '#2b4972', '#c54100',
                             '#2b286f', '#69acf1', '#ffd237', '#ff7200', '#863c00', '#4f0377', '#6cbfff']
        self.zodiac_element = ['fire', 'earth', 'air', 'water', 'fire',
                               'earth', 'air', 'water', 'fire', 'earth', 'air', 'water']

        # get color configuration

        # Immediately generate template.
        self.template = self.makeTemplate()

    def __transitRing(self, r):
        # 1. Definisci un filtro con sfocatura gaussiana
        filter_id = "blur_filter"
        blur_filter = '''
        <defs>
            <filter id="%s" x="-50%%" y="-50%%" width="200%%" height="200%%">
                <feGaussianBlur in="SourceGraphic" stdDeviation="8" />
            </filter>
        </defs>
        ''' % filter_id

        # 2. Applica questo filtro al cerchio esterno
        outer_ring = '<circle class="transitRing" cx="%s" cy="%s" r="%s" style="fill: none; stroke: white; stroke-width: 40px; stroke-opacity: .8; filter: url(#%s);"/>' % (
            r, r, r, filter_id)
        
        inner_ring = '<circle class="transitRing" cx="%s" cy="%s" r="%s" style="fill: none; stroke: %s; stroke-width: 36px; stroke-opacity: 1;"/>' % (
            r, r, r-18, self.colors_settings['paper_2'])
        inner_ring += '<circle class="transitRing" cx="%s" cy="%s" r="%s" style="fill: none; stroke: %s; stroke-width: 1px; stroke-opacity: .6;"/>' % (
            r, r, r, self.colors_settings['zodiac_transit_ring_3'])

        return blur_filter + outer_ring + inner_ring

    # draw degree ring
    def __degreeRing(self, r):
        out = ''
        for i in range(72):
            offset = float(i*5) - self.houses_degree_ut[6]
            if offset < 0:
                offset = offset + 360.0
            elif offset > 360:
                offset = offset - 360.0
            x1 = self.__sliceToX(0, r-self.c1, offset) + self.c1
            y1 = self.__sliceToY(0, r-self.c1, offset) + self.c1
            x2 = self.__sliceToX(0, r+2-self.c1, offset) - 2 + self.c1
            y2 = self.__sliceToY(0, r+2-self.c1, offset) - 2 + self.c1
            out += '<line x1="%s" y1="%s" x2="%s" y2="%s" style="stroke: %s; stroke-width: 1px; stroke-opacity:.9;"/>' % (
                x1, y1, x2, y2, self.colors_settings['paper_0'])
        return out

    def __degreeTransitRing(self, r):
        out = ''
        for i in range(72):
            offset = float(i*5) - self.houses_degree_ut[6]
            if offset < 0:
                offset = offset + 360.0
            elif offset > 360:
                offset = offset - 360.0
            x1 = self.__sliceToX(0, r, offset)
            y1 = self.__sliceToY(0, r, offset)
            x2 = self.__sliceToX(0, r+2, offset) - 2
            y2 = self.__sliceToY(0, r+2, offset) - 2
            out += '<line x1="%s" y1="%s" x2="%s" y2="%s" style="stroke: #F00; stroke-width: 1px; stroke-opacity:.9;"/>' % (
                x1, y1, x2, y2)
        return out

    # floating latitude an longitude to string
    def __lat2str(self, coord):
        sign = self.language_settings["north"]
        if coord < 0.0:
            sign = self.language_settings["south"]
            coord = abs(coord)
        deg = int(coord)
        min = int((float(coord) - deg) * 60)
        sec = int(round(float(((float(coord) - deg) * 60) - min) * 60.0))
        return "%s°%s'%s\" %s" % (deg, min, sec, sign)

    def __lon2str(self, coord):
        sign = self.language_settings["east"]
        if coord < 0.0:
            sign = self.language_settings["west"]
            coord = abs(coord)
        deg = int(coord)
        min = int((float(coord) - deg) * 60)
        sec = int(round(float(((float(coord) - deg) * 60) - min) * 60.0))
        return "%s°%s'%s\" %s" % (deg, min, sec, sign)

    # join hour, minutes, seconds, timezone integere to hour float
    def __decHourJoin(self, inH, inM, inS):
        dh = float(inH)
        dm = float(inM)/60
        ds = float(inS)/3600
        output = dh + dm + ds
        return output

    # Datetime offset to float in hours
    def __offsetToTz(self, dtoffset):
        dh = float(dtoffset.days * 24)
        sh = float(dtoffset.seconds / 3600.0)
        output = dh + sh
        return output

    # degree difference
    def __degreeDiff(self, a, b):
        out = float()
        if a > b:
            out = a - b
        if a < b:
            out = b-a
        if out > 180.0:
            out = 360.0-out
        return out

    # decimal to degrees (a°b'c")
    def __dec2deg(self, dec, type="3"):
        dec = float(dec)
        a = int(dec)
        a_new = (dec-float(a)) * 60.0
        b_rounded = int(round(a_new))
        b = int(a_new)
        c = int(round((a_new-float(b))*60.0))
        if type == "3":
            out = '%(#1)02d&#176;%(#2)02d&#39;%(#3)02d&#34;' % {
                '#1': a, '#2': b, '#3': c}
        elif type == "2":
            out = '%(#1)02d&#176;%(#2)02d&#39;' % {'#1': a, '#2': b_rounded}
        elif type == "1":
            out = '%(#1)02d' % {'#1': a}
        return str(out)

    # draw svg aspects: ring, aspect ring, degreeA degreeB
    def __drawAspect(self, r, ar, aspect_dict, aspect_id: str, color: str, isAxis=False, cut_by=8.4):
        degA= aspect_dict['p1_abs_pos']
        degB = aspect_dict['p2_abs_pos']
        orb = aspect_dict['orbit'] if not isAxis else None
        offset = (int(self.houses_degree_ut[6]) / -1) + int(degA)
        x1 = self.__sliceToX(0, ar, offset) + (r - ar)
        y1 = self.__sliceToY(0, ar, offset) + (r - ar)
        offset = (int(self.houses_degree_ut[6]) / -1) + int(degB)
        x2 = self.__sliceToX(0, ar, offset) + (r - ar)
        y2 = self.__sliceToY(0, ar, offset) + (r - ar)
        stroke_opacity = '1'
        if isAxis:
            width = x2 - x1
            height = y2 - y1
            start = {'x': x1, 'y': y1}
            end = {'x': x2, 'y': y2}
            
            # If the line is vertical
            if width == 0:
                ratio = height / cut_by
                firstCut = {'x': start['x'], 'y': start['y'] + ratio}
                lastCut = {'x': end['x'], 'y': end['y'] - ratio}
            # If the line isn't vertical
            else:
                ratio = width / cut_by
                firstCut = {'x': start['x'] + ratio, 'y': start['y'] + (height / width) * ratio}
                lastCut = {'x': end['x'] - ratio, 'y': end['y'] - (height / width) * ratio}
            label = 'Asc' if 'Ascendant' in aspect_id else 'Mc'
            add_arrow = f'marker-start: url(#arrowhead{label}{color});'
        else:
            add_arrow = ''
        if isAxis:
            axis_stroke_width = '2.5'
            axis_stroke_opacity = '.7'
            line = f'''
                <g class="axis" id="{aspect_id}" style="stroke-width: {axis_stroke_width}; stroke-opacity: {axis_stroke_opacity}; transform: translate(0, 0);" stroke-linecap="round" >
                    <line x1="{start["x"]}" y1="{start["y"]}" x2="{firstCut["x"]}" y2="{firstCut["y"]}" style="stroke: {color}; {add_arrow}" />
                    <line x1="{firstCut["x"]}" y1="{firstCut["y"]}" x2="{lastCut["x"]}" y2="{lastCut["y"]}" style="stroke: none; stroke-opacity: 0;" />
                    <line x1="{lastCut["x"]}" y1="{lastCut["y"]}" x2="{end["x"]}" y2="{end["y"]}" style="stroke: {color};"/>
                </g>
            '''
        else:
            if orb:
                if self.chart_type == 'Composite' or self.chart_type == 'Transit':
                    width_max = 1
                    width_min = 1
                else:
                    width_max = 5
                    width_min = 1
                max_orb = 5
                aspect_stroke_width = max(width_min, min(width_max, width_max - (abs(orb) / max_orb) * (width_max - width_min)))
            else:
                aspect_stroke_width = '1.5'
            line = f'<line class="aspect" id="{aspect_id}" x1="' + str(x1) + '" y1="' + str(y1) + '" x2="' + str(x2) + '" y2="' + str(
                y2) + '" style="stroke: ' + color + f'; stroke-width: {aspect_stroke_width}; stroke-opacity: {stroke_opacity};" stroke-linecap="round" />'
        if not isAxis:
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            dx = x2 - x1
            dy = y2 - y1
            angle = math.atan2(dy, dx) * 180 / math.pi
            if angle < 0:
                angle += 360
            label_offset = 10
            if (0 <= angle < 45) or (315 <= angle < 360):
                mid_y += label_offset
            elif (45 <= angle < 135):
                if aspect_dict['aspect'] == 'conjunction' and 270 > degA > 90:
                    mid_x -= label_offset
                else:
                    mid_x += label_offset
            elif (135 <= angle < 225):
                if aspect_dict['aspect'] == 'conjunction' and 270 > degA > 90:
                    mid_y += label_offset
                else:
                    mid_y -= label_offset
            else:
                mid_x -= label_offset
            line += f'<text class="aspectDeg" id="{aspect_id}Deg" x="{mid_x}" y="{mid_y}" fill="#ffffff" text-anchor="middle" dominant-baseline="middle" style="opacity: 0; font-size: .7em">{str(round(orb))}°</text>'
        return line

    def __sliceToX(self, slice, r, offset):
        plus = (math.pi * offset) / 180
        radial = ((math.pi/6) * slice) + plus
        return r * (math.cos(radial)+1)

    def __sliceToY(self, slice, r, offset):
        plus = (math.pi * offset) / 180
        radial = ((math.pi/6) * slice) + plus
        return r * ((math.sin(radial)/-1)+1)

    def __zodiacSlice(self, num, r, style,  type: str):
        offset = 360 - self.houses_degree_ut[6] + num * 30
        next_offset = offset + 30
        # check transit
        if self.chart_type == "Transit" or self.chart_type == "Composite":
            dropin = 0
            roff = 72
        else:
            dropin = self.c1
            roff = self.c2
        x1 = self.__sliceToX(0, (r-dropin), offset) + dropin
        y1 = self.__sliceToY(0, (r-dropin), offset) + dropin
        x2 = self.__sliceToX(0, r-roff, offset) + roff
        y2 = self.__sliceToY(0, r-roff, offset) + roff
        x3 = self.__sliceToX(0, (r-dropin), next_offset) + dropin
        y3 = self.__sliceToY(0, (r-dropin), next_offset) + dropin
        x4 = self.__sliceToX(0, r-roff, next_offset) + roff
        y4 = self.__sliceToY(0, r-roff, next_offset) + roff
        # Inizia al bordo inferiore della cuspide della casa corrente
        path_data = f"M {x1},{y1} "
        # Vai al bordo superiore lungo la cuspide
        path_data += f"L {x2},{y2} "
        # Segui l'arco superiore alla prossima cuspide
        path_data += f"A {r-roff},{r-roff} 0 0,0 {x4},{y4} "
        # Vai al bordo inferiore lungo la cuspide
        path_data += f"L {x3},{y3} "
        # Segui l'arco inferiore indietro alla cuspide della casa corrente
        path_data += f"A {r-dropin},{r-dropin} 0 0,1 {x1},{y1} "
        # Chiudi il percorso (anche se non necessario perché le coordinate finali e iniziali coincidono)
        path_data += "Z"
        slice = f'<path d="{path_data}" class="zodiac" id="{type.title()[:3]} slice" style="{style}"/>'
        # symbols
        offset = offset + 15
        # check transit
        if self.chart_type == "Transit" or self.chart_type == "Composite":
            dropin = 54
        else:
            dropin = 18+self.c1
        sign_x = dropin + self.__sliceToX(0, r-dropin, offset)
        sign_y = dropin + self.__sliceToY(0, r-dropin, offset)
        sign = f'<g class="sign" id="{type.title()[:3]}" transform="translate(-10,-11)"><use x="{sign_x}" y="{sign_y}" xlink:href="#{type}" /></g>'
        return slice + sign

    def __makeZodiac(self, r):
        output = ""
        for i in range(len(self.zodiac)):
            output = output + self.__zodiacSlice(i, r, "fill:" + self.colors_settings["zodiac_bg_%s" % (
                i)] + "; fill-opacity: 1; fill-opacity: 1; stroke:#FFFFFF; stroke-opacity: 1; stroke-width: 2;", self.zodiac[i]) + ''
        return output

    def __makeHouses(self, r):
        path = ""
        house_by_index = {
            1: 'First',
            2: 'Second',
            3: 'Third',
            4: 'Fourth',
            5: 'Fifth',
            6: 'Sixth',
            7: 'Seventh',
            8: 'Eighth',
            9: 'Ninth',
            10: 'Tenth',
            11: 'Eleventh',
            12: 'Twelfth'
        }
        xr = 12
        for i in range(xr):
            if self.chart_type == "Transit" or self.chart_type == "Composite":
                dropin = 160
                roff = 72
                t_roff = 36
            else:
                dropin = self.c3
                roff = self.c2

            offset = (int(self.houses_degree_ut[int(xr/2)]) / -1) + int(self.houses_degree_ut[i])
            x1 = self.__sliceToX(0, (r-dropin), offset) + dropin
            y1 = self.__sliceToY(0, (r-dropin), offset) + dropin
            x2 = self.__sliceToX(0, r-roff, offset) + roff
            y2 = self.__sliceToY(0, r-roff, offset) + roff

            if i < (xr-1):
                text_offset = offset + int(self.__degreeDiff(self.houses_degree_ut[(i+1)], self.houses_degree_ut[i]) / 6)
                next_offset = (int(self.houses_degree_ut[int(xr/2)]) / -1) + int(self.houses_degree_ut[i+1])
            else:
                text_offset = offset + int(self.__degreeDiff(self.houses_degree_ut[0], self.houses_degree_ut[(xr-1)]) / 6)
                next_offset = (int(self.houses_degree_ut[int(xr/2)]) / -1) + int(self.houses_degree_ut[0])

            linecolor = self.colors_settings['houses_radix_line']
            
            if i+1 == 1:
                house_number = 'I'
            elif i+1 == 4:
                house_number = 'IV'
            elif i+1 == 7:
                house_number = 'VII'
            elif i+1 == 10:
                house_number = 'X'
            else:
                house_number = i+1

            # Transit houses lines.
            if self.chart_type == "Transit" or self.chart_type == "Composite":
                zeropoint = 360 - self.houses_degree_ut[6]
                t_offset = zeropoint + self.t_houses_degree_ut[i]
                if t_offset > 360:
                    t_offset = t_offset - 360
                t_x1 = self.__sliceToX(0, (r-t_roff), t_offset) + t_roff
                t_y1 = self.__sliceToY(0, (r-t_roff), t_offset) + t_roff
                t_x2 = self.__sliceToX(0, r, t_offset)
                t_y2 = self.__sliceToY(0, r, t_offset)

                if i < 11:
                    t_text_offset = t_offset + int(self.__degreeDiff(self.t_houses_degree_ut[(i+1)], self.t_houses_degree_ut[i]) / 2)
                    next_t_offset = zeropoint + self.t_houses_degree_ut[i+1]
                else:
                    t_text_offset = t_offset + int(self.__degreeDiff(self.t_houses_degree_ut[0], self.t_houses_degree_ut[11]) / 2)
                    next_t_offset = zeropoint + self.t_houses_degree_ut[0]

                if next_t_offset > 360:
                    t_text_offset = t_offset + int(self.__degreeDiff(self.t_houses_degree_ut[0], self.t_houses_degree_ut[11]) / 2)
                    next_t_offset = next_t_offset - 360

                t_x3 = self.__sliceToX(0, (r-t_roff), next_t_offset) + t_roff
                t_y3 = self.__sliceToY(0, (r-t_roff), next_t_offset) + t_roff
                t_x4 = self.__sliceToX(0, r, next_t_offset)
                t_y4 = self.__sliceToY(0, r, next_t_offset)

                t_path_data = f"M {t_x1},{t_y1} " \
                            f"L {t_x2},{t_y2} " \
                            f"A {r},{r} 0 0,0 {t_x4},{t_y4} " \
                            f"L {t_x3},{t_y3} " \
                            f"A {r-t_roff},{r-t_roff} 0 0,1 {t_x1},{t_y1} Z"
                            
                t_linecolor = linecolor
                text_k = 25
                text_x_k = -3
                text_y_k = +6
                xtext = self.__sliceToX(0, (r-text_k), t_text_offset-12) + text_k + text_x_k
                ytext = self.__sliceToY(0, (r-text_k), t_text_offset-12) + text_k + text_y_k

                path_opacity = "0" if self.chart_type == "Transit" else ".4"
                path = path + f'<path d="{t_path_data}" style="stroke: {t_linecolor}; stroke-width: 1px; stroke-opacity:{path_opacity}; fill: none" class="house" id="{house_by_index[i+1]} House Transit"/>'
                text_opacity = "0" if self.chart_type == "Transit" else ".8"
                path = path + f'<text class="houseLabel" id="{house_by_index[i+1]} House Label Transit" style="fill: #000000; fill-opacity: {text_opacity}; font-size: .7em; font-family: Cinzel; font-weight: bold"><tspan x="{xtext}" y="{ytext}">{house_number}</tspan></text>'

            if self.chart_type == 'Transit' or self.chart_type == 'Composite':
                text_k = 110
            else:
                text_k = 85
            xtext = self.__sliceToX(0, (r-text_k), text_offset) + text_k - 5
            ytext = self.__sliceToY(0, (r-text_k), text_offset) + text_k + 5
            x3 = self.__sliceToX(0, (r-dropin), next_offset) + dropin
            y3 = self.__sliceToY(0, (r-dropin), next_offset) + dropin
            x4 = self.__sliceToX(0, r-roff, next_offset) + roff
            y4 = self.__sliceToY(0, r-roff, next_offset) + roff
            # Inizia al bordo inferiore della cuspide della casa corrente
            path_data = f"M {x1},{y1} "
            # Vai al bordo superiore lungo la cuspide
            path_data += f"L {x2},{y2} "
            # Segui l'arco superiore alla prossima cuspide
            path_data += f"A {r-roff},{r-roff} 0 0,0 {x4},{y4} "
            # Vai al bordo inferiore lungo la cuspide
            path_data += f"L {x3},{y3} "
            # Segui l'arco inferiore indietro alla cuspide della casa corrente
            path_data += f"A {r-dropin},{r-dropin} 0 0,1 {x1},{y1} "
            # Chiudi il percorso (anche se non necessario perché le coordinate finali e iniziali coincidono)
            path_data += "Z"
            path = path + '<path d="'+path_data+f'" class="house" id="{house_by_index[i+1]} House" fill="white" style="stroke: '+linecolor+'; stroke-width: 1px; stroke-opacity:.4;"/>'
            path = path + f'<text class="houseLabel" id="{house_by_index[i+1]} House Label" style="fill: #000000; fill-opacity: .8; font-size: .7em; font-family: Cinzel; font-weight: bold"><tspan x="' + \
                str(xtext)+'" y="'+str(ytext) + \
                '">'+str(house_number)+'</tspan></text>'
        return path

    def __makeDegrees(self, r):
        output = ""
        for i in range(len(self.zodiac)):
            output = output + self.__signDegrees(r, i, self.zodiac[i])
        return output

    def __signDegrees(self, r, num, sign):
        degrees = ''
        if self.chart_type == 'Transit' or self.chart_type == 'Composite':
            c2 = self.c2 + 35
        else:
            c2 = self.c2
        for i in range(num*30, (num+1)*30):
            offset_degree = i - self.houses_degree_ut[6]
            if offset_degree < 0:
                offset_degree += 360
            elif offset_degree > 360:
                offset_degree -= 360
            length = 5 if i % 5 == 0 else 3
            dx1 = self.__sliceToX(0, r-c2, offset_degree) + c2
            dy1 = self.__sliceToY(0, r-c2, offset_degree) + c2
            dx2 = self.__sliceToX(0, r-length-c2, offset_degree) + length + c2
            dy2 = self.__sliceToY(0, r-length-c2, offset_degree) + length + c2
            degrees += f'<line class="{sign.title()[:3]} degree" x1="{dx1}" y1="{dy1}" x2="{dx2}" y2="{dy2}" style="stroke: {self.colors_settings["paper_0"]}; stroke-width: 1px; stroke-opacity: 1;"/>'
        return degrees

    def __makePlanets(self, r):

        planets_degut = {}

        diff = range(len(self.planets_settings))
        for i in range(len(self.planets_settings)):
            if self.planets_settings[i]['visible'] == 1:
                # list of planets sorted by degree
                planets_degut[self.planets_degree_ut[i]] = i

            # element: get extra points if planet is in own zodiac
            pz = self.planets_settings[i]['zodiac_relation']
            cz = self.planets_sign[i]
            extrapoints = 0
            if pz != -1:
                for e in range(len(pz.split(','))):
                    if int(pz.split(',')[e]) == int(cz):
                        extrapoints = 10

            # calculate element points for all planets
            ele = self.zodiac_element[self.planets_sign[i]]
            if ele == "fire":
                self.fire = self.fire + \
                    self.planets_settings[i]['element_points'] + extrapoints
            elif ele == "earth":
                self.earth = self.earth + \
                    self.planets_settings[i]['element_points'] + extrapoints
            elif ele == "air":
                self.air = self.air + \
                    self.planets_settings[i]['element_points'] + extrapoints
            elif ele == "water":
                self.water = self.water + \
                    self.planets_settings[i]['element_points'] + extrapoints

        output = ""
        keys = list(planets_degut.keys())
        keys.sort()
        switch = 0

        groups = []

        def zero(x): return 0
        planets_delta = list(map(zero, range(len(self.planets_settings))))

        used_degrees = []
        threshold = 6
        for e in range(len(keys)):
            i = planets_degut[keys[e]]
            if self.chart_type == "Transit" or self.chart_type == "Composite":
                c = self.c4
            else:
                c = self.c4
            rotate = self.houses_degree_ut[0] - self.planets_degree_ut[i]
            textanchor = "end"
            rtext = -9
            if -90 > rotate > -270:
                rotate = rotate + 180.0
                textanchor = "start"
            if 270 > rotate > 90:
                rotate = rotate - 180.0
                textanchor = "start"
            if textanchor == 'end':
                xo = 1
            else:
                xo = -1
            # Add tick marks for inner planets
            offset = (int(self.houses_degree_ut[6]) / -1) + int(self.planets_degree_ut[i])
            
            # Controlla se il grado è troppo vicino a un grado già utilizzato
            too_close = False
            # for used in used_degrees:
            #     if abs(offset - used) < threshold:
            #         too_close = True
            #         break
                        
            x1 = self.__sliceToX(0, r-c, offset) + c
            y1 = self.__sliceToY(0, r-c, offset) + c
            length = 7
            x2 = self.__sliceToX(0, r+length-c, offset) - length + c
            y2 = self.__sliceToY(0, r+length-c, offset) - length + c
            
            # Add the line to the output
            output = output + f'<line id="{self.planets_settings[i]["name"].title()}GLine" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" style="stroke: white; stroke-width: 1px; stroke-opacity:.8;"/>'

            if not too_close:
                # Aggiungi il grado alla lista dei gradi utilizzati
                used_degrees.append(offset)

                # Calculate positions for the degree text
                deg_x = self.__sliceToX(0, (r-c-rtext), offset + xo) + rtext + c
                deg_y = self.__sliceToY(0, (r-c-rtext), offset + xo) + rtext + c
                
                # Add the degree text to the output
                output += f'<g transform="translate({deg_x}, {deg_y})" id="{self.planets_settings[i]["name"].title()}GLineText">'
                output += f'<text transform="rotate({rotate})" text-anchor="{textanchor}" style="fill: white; font-size: .7em;">'
                output += f'{self.__dec2deg(self.planets_degree[i], type="1")}'
                output += '</text></g>'

            # coordinates
            if self.chart_type == "Transit" or self.chart_type == "Composite":
                rplanet = 95
            else:
                rplanet = 60
            rtext = 45
            offset = (int(self.houses_degree_ut[6]) / -1) + \
                int(self.planets_degree_ut[i]+planets_delta[e])

            planet_x = self.__sliceToX(0, (r-rplanet), offset) + rplanet
            planet_y = self.__sliceToY(0, (r-rplanet), offset) + rplanet
            if self.chart_type == "Transit" or self.chart_type == "Composite":
                scale = 1.1
            else:
                scale = 1.1
            # output planet
            if self.planets_retrograde[i]:
                output += f'''
                    <g id="{self.planets_settings[i]["name"].title()}G" transform="translate(-{str(12*scale)}, -{str(12*scale)}) scale({str(scale)})">
                        <use x="{str(planet_x*(1/scale))}" y="{str(planet_y*(1/scale))}" xlink:href="#{self.planets_settings[i]["name"]}Retrograde"/>
                    </g>'''
            else:
                output += f'''
                    <g id="{self.planets_settings[i]["name"].title()}G" transform="translate(-{str(12*scale)}, -{str(12*scale)}) scale({str(scale)})">
                        <use x="{str(planet_x*(1/scale))}" y="{str(planet_y*(1/scale))}" xlink:href="#{self.planets_settings[i]["name"]}"/>
                    </g>'''
            # Adjust the offset degree to be within 0 to 360
            if self.chart_type == 'Transit' or self.chart_type == 'Composite':
                c = self.c3 + 62.5
            else:
                c = self.c3
            # output += self.drawTick(c, r, self.planets_settings[i]["name"], offset, i)

        # make transit degut and display planets
        if self.chart_type == "Transit" or self.chart_type == "Composite":
            group_offset = {}
            t_planets_degut = {}
            list_range = len(self.planets_settings)
            for i in range(list_range):
                group_offset[i] = 0
                if self.planets_settings[i]['visible'] == 1:
                    t_planets_degut[self.t_planets_degree_ut[i]] = i
            t_keys = list(t_planets_degut.keys())
            t_keys.sort()

            # grab closely grouped planets
            groups = []
            in_group = False
            for e in range(len(t_keys)):
                i_a = t_planets_degut[t_keys[e]]
                if e == (len(t_keys)-1):
                    i_b = t_planets_degut[t_keys[0]]
                else:
                    i_b = t_planets_degut[t_keys[e+1]]

                a = self.t_planets_degree_ut[i_a]
                b = self.t_planets_degree_ut[i_b]
                diff = self.__degreeDiff(a, b)
                if diff <= 2.5:
                    if in_group:
                        groups[-1].append(i_b)
                    else:
                        groups.append([i_a])
                        groups[-1].append(i_b)
                        in_group = True
                else:
                    in_group = False
            # loop groups and set degrees display adjustment
            for i in range(len(groups)):
                if len(groups[i]) == 2:
                    group_offset[groups[i][0]] = -1.0
                    group_offset[groups[i][1]] = 1.0
                elif len(groups[i]) == 3:
                    group_offset[groups[i][0]] = -1.5
                    group_offset[groups[i][1]] = 0
                    group_offset[groups[i][2]] = 1.5
                elif len(groups[i]) == 4:
                    group_offset[groups[i][0]] = -2.0
                    group_offset[groups[i][1]] = -1.0
                    group_offset[groups[i][2]] = 1.0
                    group_offset[groups[i][3]] = 2.0

            switch = 0

            for e in range(len(t_keys)):
                i = t_planets_degut[t_keys[e]]
                if 22 < i < 27:
                    rplanet = 4
                elif switch == 1:
                    rplanet = 5
                    switch = 0
                else:
                    rplanet = 4
                    switch = 1
                zeropoint = 360 - self.houses_degree_ut[6]
                t_offset = zeropoint + self.t_planets_degree_ut[i]
                if t_offset > 360:
                    t_offset = t_offset - 360
                planet_x = self.__sliceToX(0, (r+rplanet), t_offset)
                planet_y = self.__sliceToY(0, (r+rplanet), t_offset)
                if self.t_points_retrograde[i]:
                    output = output + f'<g><g id="{self.planets_settings[i]["name"].title()}GTransit" transform="scale(0.9) translate(15, 15)"><use x="' + str(planet_x) + '" y="' + str(planet_y) + '" xlink:href="#' + self.planets_settings[i]['name'] + 'Retrograde" /></g></g>'
                else:
                    output = output + f'<g><g id="{self.planets_settings[i]["name"].title()}GTransit" transform="scale(0.9) translate(15, 15)"><use x="' + str(planet_x) + '" y="' + str(planet_y) + '" xlink:href="#' + self.planets_settings[i]['name'] + '" /></g></g>'
                                
                # transit planet line
                x1 = self.__sliceToX(0, r+3, t_offset) - 3
                y1 = self.__sliceToY(0, r+3, t_offset) - 3
                x2 = self.__sliceToX(0, r-3, t_offset) + 3
                y2 = self.__sliceToY(0, r-3, t_offset) + 3
                output = output + f'<line id="{self.planets_settings[i]["name"].title()}GTransitLine" x1="'+str(x1)+'" y1="'+str(y1)+'" x2="'+str(x2)+'" y2="'+str(
                    y2)+'" style="stroke: red'+'; stroke-width: 1px; stroke-opacity:.8;"/>'

                # transit planet line for inner circle
                length = 7
                x1_inner = self.__sliceToX(0, r-self.c4, t_offset) + self.c4
                y1_inner = self.__sliceToY(0, r-self.c4, t_offset) + self.c4
                x2_inner = self.__sliceToX(0, r-self.c4+length, t_offset) + self.c4 - length
                y2_inner = self.__sliceToY(0, r-self.c4+length, t_offset) + self.c4 - length
                output = output + f'<line id="{self.planets_settings[i]["name"].title()}GTransitLineInner" x1="'+str(x1_inner)+'" y1="'+str(y1_inner)+'" x2="'+str(x2_inner)+'" y2="'+str(y2_inner)+'" style="stroke: red'+'; stroke-width: 1px; stroke-opacity:.8;"/>'

                # transit planet degree text
                rotate = self.houses_degree_ut[0] - self.t_planets_degree_ut[i]
                textanchor = "end"
                t_offset += group_offset[i]
                rtext = -5.0

                if -90 > rotate > -270:
                    rotate = rotate + 180.0
                    textanchor = "start"
                if 270 > rotate > 90:
                    rotate = rotate - 180.0
                    textanchor = "start"

                if textanchor == "end":
                    xo = 1
                else:
                    xo = -1
                deg_x = self.__sliceToX(0, (r-rtext), t_offset + xo) + rtext
                deg_y = self.__sliceToY(0, (r-rtext), t_offset + xo) + rtext
                output += f'<g id="{self.planets_settings[i]["name"].title()}GTransitLineText" transform="translate({deg_x}, {deg_y})">'
                output += '<text transform="rotate(%s)" text-anchor="%s' % (
                    rotate, textanchor)
                output += '" style="fill: black' + \
                    '; font-size: .7em;">' + \
                    self.__dec2deg(self.t_planets_degree[i], type="1")
                output += '</text></g>'

            # check transit
            if self.chart_type == "Transit" or self.chart_type == "Composite":
                dropin = 36
            else:
                dropin = 0

            # planet line
            x1 = self.__sliceToX(0, r-(dropin+3), offset) + (dropin+3)
            y1 = self.__sliceToY(0, r-(dropin+3), offset) + (dropin+3)
            x2 = self.__sliceToX(0, (r-(dropin-3)), offset) + (dropin-3)
            y2 = self.__sliceToY(0, (r-(dropin-3)), offset) + (dropin-3)
            output = output + '<line x1="'+str(x1)+'" y1="'+str(y1)+'" x2="'+str(x2)+'" y2="'+str(
                y2)+'" style="stroke: '+self.planets_settings[i]['color']+'; stroke-width: 2px; stroke-opacity:.6;"/>'

            # check transit
            if self.chart_type == "Transit" or self.chart_type == "Composite":
                dropin = 160
            else:
                dropin = 120

            x1 = self.__sliceToX(0, r-dropin, offset) + dropin
            y1 = self.__sliceToY(0, r-dropin, offset) + dropin
            x2 = self.__sliceToX(0, (r-(dropin-3)), offset) + (dropin-3)
            y2 = self.__sliceToY(0, (r-(dropin-3)), offset) + (dropin-3)
            output = output + '<line x1="'+str(x1)+'" y1="'+str(y1)+'" x2="'+str(x2)+'" y2="'+str(
                y2)+'" style="stroke: '+self.planets_settings[i]['color']+'; stroke-width: 2px; stroke-opacity:.6;"/>'
        return output

    def __makePatterns(self):
        """
        * Stellium: At least four planets linked together in a series of continuous conjunctions.
        * Grand trine: Three trine aspects together.
        * Grand cross: Two pairs of opposing planets squared to each other.
        * T-Square: Two planets in opposition squared to a third.
        * Yod: Two qunicunxes together joined by a sextile.
        """
        conj = {}  # 0
        opp = {}  # 10
        sq = {}  # 5
        tr = {}  # 6
        qc = {}  # 9
        sext = {}  # 3
        for i in range(len(self.planets_settings)):            
            a = self.planets_degree_ut[i]
            qc[i] = {}
            sext[i] = {}
            opp[i] = {}
            sq[i] = {}
            tr[i] = {}
            conj[i] = {}
            # skip some points
            n = self.planets_settings[i]['name']
            if n == 'earth' or n == 'True_Node' or n == 'osc. apogee' or n == 'intp. apogee' or n == 'intp. perigee':
                continue
            if n == 'Dsc' or n == 'Ic':
                continue
            for j in range(len(self.planets_settings)):
                # skip some points
                n = self.planets_settings[j]['name']
                if n == 'earth' or n == 'True_Node' or n == 'osc. apogee' or n == 'intp. apogee' or n == 'intp. perigee':
                    continue
                if n == 'Dsc' or n == 'Ic':
                    continue
                b = self.planets_degree_ut[j]
                delta = float(self.__degreeDiff(a, b))
                # check for opposition
                xa = float(self.aspects_settings[10]['degree']) - \
                    float(self.aspects_settings[10]['orb'])
                xb = float(self.aspects_settings[10]['degree']) + \
                    float(self.aspects_settings[10]['orb'])
                if(xa <= delta <= xb):
                    opp[i][j] = True
                # check for conjunction
                xa = float(self.aspects_settings[0]['degree']) - \
                    float(self.aspects_settings[0]['orb'])
                xb = float(self.aspects_settings[0]['degree']) + \
                    float(self.aspects_settings[0]['orb'])
                if(xa <= delta <= xb):
                    conj[i][j] = True
                # check for squares
                xa = float(self.aspects_settings[5]['degree']) - \
                    float(self.aspects_settings[5]['orb'])
                xb = float(self.aspects_settings[5]['degree']) + \
                    float(self.aspects_settings[5]['orb'])
                if(xa <= delta <= xb):
                    sq[i][j] = True
                # check for qunicunxes
                xa = float(self.aspects_settings[9]['degree']) - \
                    float(self.aspects_settings[9]['orb'])
                xb = float(self.aspects_settings[9]['degree']) + \
                    float(self.aspects_settings[9]['orb'])
                if(xa <= delta <= xb):
                    qc[i][j] = True
                # check for sextiles
                xa = float(self.aspects_settings[3]['degree']) - \
                    float(self.aspects_settings[3]['orb'])
                xb = float(self.aspects_settings[3]['degree']) + \
                    float(self.aspects_settings[3]['orb'])
                if(xa <= delta <= xb):
                    sext[i][j] = True

        yot = {}
        # check for double qunicunxes
        for k, v in qc.items():
            if len(qc[k]) >= 2:
                # check for sextile
                for l, w in qc[k].items():
                    for m, x in qc[k].items():
                        if m in sext[l]:
                            if l > m:
                                yot['%s,%s,%s' % (k, m, l)] = [k, m, l]
                            else:
                                yot['%s,%s,%s' % (k, l, m)] = [k, l, m]
        tsquare = {}
        # check for opposition
        for k, v in opp.items():
            if len(opp[k]) >= 1:
                # check for square
                for l, w in opp[k].items():
                    for a, b in sq.items():
                        if k in sq[a] and l in sq[a]:
                            # print 'got tsquare %s %s %s' % (a,k,l)
                            if k > l:
                                tsquare['%s,%s,%s' % (a, l, k)] = '%s => %s, %s' % (
                                    self.planets_settings[a]['label'], self.planets_settings[l]['label'], self.planets_settings[k]['label'])
                            else:
                                tsquare['%s,%s,%s' % (a, k, l)] = '%s => %s, %s' % (
                                    self.planets_settings[a]['label'], self.planets_settings[k]['label'], self.planets_settings[l]['label'])
        stellium = {}
        # check for 4 continuous conjunctions
        for k, v in conj.items():
            if len(conj[k]) >= 1:
                # first conjunction
                for l, m in conj[k].items():
                    if len(conj[l]) >= 1:
                        for n, o in conj[l].items():
                            # skip 1st conj
                            if n == k:
                                continue
                            if len(conj[n]) >= 1:
                                # third conjunction
                                for p, q in conj[n].items():
                                    # skip first and second conj
                                    if p == k or p == n:
                                        continue
                                    if len(conj[p]) >= 1:
                                        # fourth conjunction
                                        for r, s in conj[p].items():
                                            # skip conj 1,2,3
                                            if r == k or r == n or r == p:
                                                continue

                                            l = [k, n, p, r]
                                            l.sort()
                                            stellium['%s %s %s %s' % (l[0], l[1], l[2], l[3])] = '%s %s %s %s' % (
                                                self.planets_settings[l[0]
                                                                      ]['label'], self.planets_settings[l[1]]['label'],
                                                self.planets_settings[l[2]]['label'], self.planets_settings[l[3]]['label'])
        # print yots
        out = '<g transform="translate(-30,380)">'
        if len(yot) >= 1:
            y = 0
            for k, v in yot.items():
                out += '<text y="%s" style="fill:%s; font-size: 12px;">%s</text>' % (
                    y, self.colors_settings['paper_0'], ("Yot"))

                # first planet symbol
                out += '<g transform="translate(20,%s)">' % (y)
                out += '<use transform="scale(0.4)" x="0" y="-20" xlink:href="#%s" /></g>' % (
                    self.planets_settings[yot[k][0]]['name'])

                # second planet symbol
                out += '<g transform="translate(30,%s)">' % (y)
                out += '<use transform="scale(0.4)" x="0" y="-20" xlink:href="#%s" /></g>' % (
                    self.planets_settings[yot[k][1]]['name'])

                # third planet symbol
                out += '<g transform="translate(40,%s)">' % (y)
                out += '<use transform="scale(0.4)" x="0" y="-20" xlink:href="#%s" /></g>' % (
                    self.planets_settings[yot[k][2]]['name'])

                y = y+14
        # finalize
        out += '</g>'
        # return out
        return ''

    # Aspect and aspect grid functions for natal type charts.

    def __makeAspects(self, r, ar):
        out = ""
        for aspect_dict in self.aspects_list:
            aspect_id = f"{min(aspect_dict['p1_name'], aspect_dict['p2_name'])}{aspect_dict['aspect'].title()}{max(aspect_dict['p1_name'], aspect_dict['p2_name'])}"
            out += self.__drawAspect(r, ar, aspect_dict, aspect_id, self.colors_settings[f"aspect_{aspect_dict['aspect_degrees']}"])
        return out

    def __makeAspectGrid(self, r):

        out = ""
        style = 'stroke:%s; stroke-width: 1px; stroke-opacity:.6; fill:none' % (
            self.colors_settings['paper_0'])
        xindent = 380
        yindent = 468
        box = 14
        revr = list(range(len(self.planets_settings)))
        revr.reverse()
        counter = 0
        for a in revr:
            counter += 1
            if self.planets_settings[a]['visible'] == 1:
                out += '<rect x="'+str(xindent)+'" y="'+str(yindent)+'" width="'+str(
                    box)+'" height="'+str(box)+'" style="'+style+'"/>'
                out += '<use transform="scale(0.4)" x="'+str((xindent+2)*2.5)+'" y="'+str(
                    (yindent+1)*2.5)+'" xlink:href="#'+self.planets_settings[a]['name']+'" />'
                xindent = xindent + box
                yindent = yindent - box
                revr2 = list(range(a))
                revr2.reverse()
                xorb = xindent
                yorb = yindent + box
                for b in revr2:
                    if self.planets_settings[b]['visible'] == 1:
                        out += '<rect x="'+str(xorb)+'" y="'+str(yorb)+'" width="'+str(
                            box)+'" height="'+str(box)+'" style="'+style+'"/>'
                        xorb = xorb+box
                        for element in self.aspects_list:
                            if (element['p1'] == a and element['p2'] == b) or (element['p1'] == b and element['p2'] == a):
                                out += '<use  x="'+str(xorb-box+1)+'" y="'+str(
                                    yorb+1)+'" xlink:href="#orb'+str(element['aspect_degrees'])+'" />'

        return out

    # Aspect and aspect grid functions for transit type charts.

    def __makeAspectsTransit(self, r, ar):
        out = ""

        self.aspects_list = CompositeAspects(
            self.t_user, self.user, settings=self.settings
        ).get_relevant_aspects()
        for aspect_dict in self.aspects_list:
            aspect_id = f"{aspect_dict['p1_name']}Transit{aspect_dict['aspect'].title()}{aspect_dict['p2_name']}Natal"
            out += self.__drawAspect(r, ar, aspect_dict, aspect_id, self.colors_settings[f"aspect_{aspect_dict['aspect_degrees']}"])

        return out

    def __makeAspectTransitGrid(self, r):
        out = '<g transform="translate(500,310)">'
        out += '<text y="-15" x="0" style="fill:%s; font-size: 14px;">%s</text>' % (
            self.colors_settings['paper_0'], (f"{self.language_settings['aspects']}:"))
        line = 0
        nl = 0
        for i in range(len(self.aspects_list)):
            if i == 12:
                nl = 100
                # if len(self.aspects_list) > 24:
                #     line = -1 * ( len(self.aspects_list) - 24) * 14
                # else:
                #     line = 0

                # temporary:
                line = 0

            if i == 24:
                nl = 200
                # if len(self.aspects_list) > 36:
                #     line = -1 * ( len(self.aspects_list) - 36) * 14
                # else:
                #     line = 0
                line = 0

            if i == 36:
                nl = 300
                if len(self.aspects_list) > 48:
                    line = -1 * (len(self.aspects_list) - 48) * 14
                else:
                    line = 0
            out += '<g transform="translate(%s,%s)">' % (nl, line)
            # first planet symbol
            out += '<use transform="scale(0.4)" x="0" y="3" xlink:href="#%s" />' % (
                self.planets_settings[self.aspects_list[i]['p1']]['name'])
            # aspect symbol
            out += '<use  x="15" y="0" xlink:href="#orb%s" />' % (
                self.aspects_settings[self.aspects_list[i]['aid']]['degree'])
            # second planet symbol
            out += '<g transform="translate(30,0)">'
            out += '<use transform="scale(0.4)" x="0" y="3" xlink:href="#%s" />' % (
                self.planets_settings[self.aspects_list[i]['p2']]['name'])
            out += '</g>'
            # difference in degrees
            out += '<text y="8" x="45" style="fill:%s; font-size: 10px;">%s</text>' % (
                self.colors_settings['paper_0'],
                self.__dec2deg(self.aspects_list[i]['orbit']))
            # line
            out += '</g>'
            line = line + 14
        out += '</g>'
        return out

    def __makeElements(self, r):
        total = self.fire + self.earth + self.air + self.water
        pf = int(round(100*self.fire/total))
        pe = int(round(100*self.earth/total))
        pa = int(round(100*self.air/total))
        pw = int(round(100*self.water/total))
        out = '<g transform="translate(-30,79)">'
        out += '<text y="0" style="fill:#ff6600; font-size: 10px;">' + \
            self.language_settings['fire']+'  '+str(pf)+'%</text>'
        out += '<text y="12" style="fill:#6a2d04; font-size: 10px;">' + \
            self.language_settings['earth']+' '+str(pe)+'%</text>'
        out += '<text y="24" style="fill:#6f76d1; font-size: 10px;">' + \
            self.language_settings['air']+'   '+str(pa)+'%</text>'
        out += '<text y="36" style="fill:#630e73; font-size: 10px;">' + \
            self.language_settings['water']+' '+str(pw)+'%</text>'
        out += '</g>'
        return out

    def __makeAxis(self, r, ar, source, cut_by, color, transit_axis):
        out = ''
        axis_stroke_opacity = '.7'
        for axis in source:
            if (transit_axis and axis.name == 'Ascendant') or (not transit_axis and axis.name in {'Ascendant', 'Midheaven'}):
                axis_data = next((ax for ax in self.axes_settings if ax['name'] == axis.name), None)
                arrow_top = f'''
                    <marker id="arrowhead{axis_data['label_short']}{color}" markerWidth="12" markerHeight="12" refX="6" refY="6" orient="auto-start-reverse">
                        <polyline points="0,2 6,6 0,10" style="fill: none; stroke: {color}; stroke-opacity: {axis_stroke_opacity}" />
                    </marker>
                '''
                if axis_data:
                    axis_id = f"{axis_data['label_short'].replace('Asc', 'Ascendant').replace('Mc', 'Midheaven')}G"
                    if transit_axis:
                        axis_id += 'Transit'
                    aspect_dict = {
                        'p1_abs_pos': axis.abs_pos,
                        'p2_abs_pos': (axis.abs_pos + 180) % 360,
                        'color': color,
                    }
                    out += arrow_top + self.__drawAspect(r, ar, aspect_dict, axis_id, color, True, cut_by)
                    offset = offset = (int(self.houses_degree_ut[6]) / -1) + int(aspect_dict['p1_abs_pos'])
                    if self.chart_type == 'Transit' or self.chart_type == 'Composite':
                        c = self.c3 + 40
                    else:
                        c = self.c3
                    index = 15 if axis.name == 'Ascendant' else 16
                    # out += self.drawTick(c, r, axis.name, offset, index)
        return out

    def drawTick(self, c, r, id, offset, i) -> str:
        out = ''
        # Calculate the start and end points of the tick mark
        tick_start_x = self.__sliceToX(0, r-c, offset) + c
        tick_start_y = self.__sliceToY(0, r-c, offset) + c
        length = 5
        tick_end_x = self.__sliceToX(0, r+length-c, offset) - length + c
        tick_end_y = self.__sliceToY(0, r+length-c, offset) - length + c
        additional_class = 'tickC3'
        tick_color = 'white'
                
        # Draw the tick mark using a line element in SVG
        out += f'''
            <g class='tick {additional_class}' id='{id}TickC4'>
                <line x1="{tick_start_x}" y1="{tick_start_y}" x2="{tick_end_x}" y2="{tick_end_y}" stroke="{tick_color}" stroke-width="1"/>
        '''
        
        out += '</g>'
        return out
    
    def __makePlanetGrid(self):
        out = '<g transform="translate(500,-20)">'

        # loop over all planets
        li = 10
        offset = 0

        out += '<g transform="translate(140, -15)">'
        out += \
            f'<text text-anchor="end" style="fill:{self.colors_settings["paper_0"]}; font-size: 14px;">{self.language_settings["planets_and_house"]} {self.name}:</text>'
        out += '</g>'

        for i in range(len(self.planets_settings)):

            # Guarda qui !!
            if i == 27:
                li = 10
                offset = -120
            if self.planets_settings[i]['visible'] == 1:
                # start of line
                out += '<g transform="translate(%s,%s)">' % (offset, li)
                # planet text
                out += f'<text text-anchor="end" style="fill:{self.colors_settings["paper_0"]}; font-size: 10px;">{self.language_settings["planets"][self.planets_settings[i]["label"]]}</text>'
                # planet symbol
                out += \
                    '<g transform="translate(5,-8)"><use transform="scale(0.4)" xlink:href="#' + \
                    self.planets_settings[i]['name']+'" /></g>'
                # planet degree
                out += '<text text-anchor="start" x="19" style="fill:%s; font-size: 10px;">%s</text>' % (
                    self.colors_settings['paper_0'], self.__dec2deg(self.planets_degree[i]))
                # zodiac
                out += '<g transform="translate(60,-8)"><use transform="scale(0.3)" xlink:href="#' + \
                    self.zodiac[self.planets_sign[i]]+'" /></g>'
                # planet retrograde
                if self.planets_retrograde[i]:
                    out += \
                        f'<g class="retrograde" transform="translate(74,-6)"><use transform="scale(.5)" xlink:href="#retrograde" /></g>'

                # end of line
                out += '</g>'
                # offset between lines
                li = li + 14

        # ----------

        if self.chart_type == "Transit" or self.chart_type == "Composite":

            if self.chart_type == "Transit":
                out += '<g transform="translate(320, -15)">'
                out += \
                    f'<text text-anchor="end" style="fill:{self.colors_settings["paper_0"]}; font-size: 14px;">{self.t_name}:</text>'
            else:
                out += '<g transform="translate(380, -15)">'
                out += \
                    f'<text text-anchor="end" style="fill:{self.colors_settings["paper_0"]}; font-size: 14px;">{self.language_settings["planets_and_house"]} {self.t_user.name}:</text>'
            out += '</g>'

            t_li = 10
            t_offset = 250

            for i in range(len(self.planets_settings)):
                if i == 27:
                    t_li = 10
                    t_offset = -120
                if self.planets_settings[i]['visible'] == 1:
                    # start of line
                    out += f'<g transform="translate({t_offset},{t_li})">'

                    # planet text
                    out += f'<text text-anchor="end" style="fill:{self.colors_settings["paper_0"]}; font-size: 10px;">{self.language_settings["planets"][self.planets_settings[i]["label"]]}</text>'
                    # planet symbol
                    out += f'<g transform="translate(5,-8)"><use transform="scale(0.4)" xlink:href="#{self.planets_settings[i]["name"]}" /></g>'
                    # planet degree
                    out += '<text text-anchor="start" x="19" style="fill:%s; font-size: 10px;">%s</text>' % (
                        self.colors_settings['paper_0'], self.__dec2deg(self.t_planets_degree[i]))
                    # zodiac
                    out += '<g transform="translate(60,-8)"><use transform="scale(0.3)" xlink:href="#' + \
                        self.zodiac[self.t_planets_sign[i]]+'" /></g>'
                    # planet retrograde
                    if self.t_planets_retrograde[i]:
                        out += \
                            '<g transform="translate(74,-6)"><use transform="scale(.5)" xlink:href="#retrograde" /></g>'

                    # end of line
                    out += '</g>'
                    # offset between lines
                    t_li = t_li + 14
        out += '</g>'

        return out

    def __makeHousesGrid(self):

        out = '<g transform="translate(600,-20)">'
        li = 10
        for i in range(12):
            if i < 9:
                cusp = '&#160;&#160;'+str(i+1)
            else:
                cusp = str(i+1)
            
            out += '<g transform="translate(0,'+str(li)+')">'
            out += '<text text-anchor="end" x="40" style="fill:%s; font-size: 10px;">%s %s:</text>' % (
                self.colors_settings['paper_0'], self.language_settings['cusp'], cusp)
            out += '<g transform="translate(40,-8)"><use transform="scale(0.3)" xlink:href="#' + \
                self.zodiac[self.houses_sign[i]]+'" /></g>'
            out += '<text x="53" style="fill:%s; font-size: 10px;"> %s</text>' % (
                self.colors_settings['paper_0'], self.__dec2deg(self.houses_list[i]["position"]))
            out += '</g>'
            li = li + 14
        out += '</g>'

        # ----------

        if self.chart_type == "Composite":
            out += '<g transform="translate(840, -20)">'
            li = 10
            for i in range(12):
                if i < 9:
                    cusp = '&#160;&#160;'+str(i+1)
                else:
                    cusp = str(i+1)
                out += '<g transform="translate(0,'+str(li)+')">'
                out += '<text text-anchor="end" x="40" style="fill:%s; font-size: 10px;">%s %s:</text>' % (
                    self.colors_settings['paper_0'], self.language_settings['cusp'], cusp)
                out += '<g transform="translate(40,-8)"><use transform="scale(0.3)" xlink:href="#' + \
                    self.zodiac[self.t_houses_sign[i]]+'" /></g>'
                out += '<text x="53" style="fill:%s; font-size: 10px;"> %s</text>' % (
                    self.colors_settings['paper_0'], self.__dec2deg(self.t_houses_list[i]["position"]))
                out += '</g>'
                li = li + 14
            out += '</g>'
        return out

    def set_output_directory(self, dir_path):
        """
        Sets the output direcotry and returns it's path.
        """
        self.output_directory = Path(dir_path)
        dir_string = f"Output direcotry set to: {self.output_directory}"
        return (print(dir_string))

    def makeTemplate(self):
        # self.chart_type = "Transit"
        # empty element points
        self.fire = 0.0
        self.earth = 0.0
        self.air = 0.0
        self.water = 0.0

        # Transit module data
        if self.chart_type == "Transit" or self.chart_type == "Composite":
            # grab transiting module data

            self.t_planets_sign = self.t_points_sign
            self.t_planets_degree = self.t_points_deg
            self.t_planets_degree_ut = self.t_points_deg_ut
            self.t_planets_retrograde = self.t_points_retrograde
            self.t_houses_list = self.t_user.houses_list
            self.t_houses_sign = self.t_houses_sign_graph
            self.t_houses_degree_ut = self.t_user.houses_degree_ut

        # grab normal module data
        self.planets_sign = self.points_sign
        self.planets_degree = self.points_deg
        self.planets_degree_ut = self.points_deg_ut
        self.planets_retrograde = self.points_retrograde
        self.houses_list = self.user.houses_list
        self.houses_sign = self.houses_sign_graph
        self.houses_degree_ut = self.user.houses_degree_ut
        self.lunar_phase = self.user.lunar_phase
        #

        # width and height from screen
        ratio = float(self.screen_width) / float(self.screen_height)
        if ratio < 1.3:  # 1280x1024
            wm_off = 130
        else:  # 1024x768, 800x600, 1280x800, 1680x1050
            wm_off = 100

        # Viewbox and sizing
        svgHeight = "100%"  # self.screen_height-wm_off
        svgWidth = "100%"  #  self.screen_width-5.0
        # svgHeight=self.screen_height-wm_off
        # svgWidth=(770.0*svgHeight)/540.0
        # svgWidth=float(self.screen_width)-25.0
        rotate = "0"
        translate = "0"
        # Defoult:
        # viewbox = '0 0 772.2 546.0' #297mm * 2.6 + 210mm * 2.6
        if self.chart_type == "Natal":
            viewbox = '0 0 772.2 546.0'  # 297mm * 2.6 + 210mm * 2.6
        else:
            viewbox = '0 0 1000 546.0'

        # template dictionary
        td = dict()
        r = 240
        if self.chart_type == "Transit" or self.chart_type == "Composite":
            self.c1 = 36
            self.c2 = 36
            self.c3 = 120
            self.c4 = 145
        else:
            self.c1 = 0
            self.c2 = 36
            self.c3 = 95
            self.c4 = 120

        # transit
        if self.chart_type == "Transit" or self.chart_type == "Composite":
            td['transitRing'] = self.__transitRing(r)
            td['transitRingAxes'] = self.__makeAxis(r, r-self.c1+53, self.t_user.axis_list, 9.7, 'black', True)
            # td['degreeRing'] = self.__degreeTransitRing(r)
            td['degreeRing'] = ''
            # circles
            td['c1'] = 'class="circle" id="c1" cx="' + str(r) + '" cy="' + \
                str(r) + '" r="' + str(r-self.c1) + '"'
            td['c1style'] = 'fill: none; stroke: %s; stroke-width: 1px; stroke-opacity:.4;' % (
                self.colors_settings['zodiac_transit_ring_2'])
            td['c2'] = 'class="circle" id="c2" cx="' + str(r) + '" cy="' + \
                str(r) + '" r="' + str(r-self.c2) + '"'
            td['c2style'] = 'fill: %s; fill-opacity: 1; stroke: %s; stroke-opacity:.4; stroke-width: 1px' % (
                self.colors_settings['paper_1'], self.colors_settings['zodiac_transit_ring_1'])
            td['c3'] = 'class="circle" id="c3" cx="' + str(r) + '" cy="' + \
                str(r) + '" r="' + str(r-self.c3) + '"'
            td['c3style'] = 'fill: %s; fill-opacity: 1; stroke: %s; stroke-width: 1px' % (
                self.colors_settings['paper_1'], self.colors_settings['zodiac_transit_ring_0'])
            td['c4'] = 'class="circle" id="c4" cx="' + str(r) + '" cy="' + \
                str(r) + '" r="' + str(r-self.c4) + '"'
            td['c4style'] = 'fill: %s; fill-opacity: 1; stroke: %s; stroke-width: 1px' % (
                self.colors_settings['paper_1'], self.colors_settings['zodiac_transit_ring_0'])
            td['makeAspects'] = self.__makeAspectsTransit(r, r-self.c4)
            td['makeAspectGrid'] = self.__makeAspectTransitGrid(r)
            td['makePatterns'] = ''
            td['makeAxis'] = self.__makeAxis(r, r-self.c1+18, self.user.axis_list, 8.4, '#ff0000', False)
            td['chart_width'] = self.full_width
        else:
            td['transitRing'] = ""
            td['transitRingAxes'] = ''
            if self.chart_type == 'minimal':
                td['degreeRing'] = ''
            else:
                td['degreeRing'] = self.__degreeRing(r)
            # circles
            td['c1'] = 'class="circle" id="c1" cx="' + str(r) + '" cy="' + \
                str(r) + '" r="' + str(r-self.c1) + '"'
            td['c1style'] = 'fill: none; stroke: %s; stroke-width: 1px; ' % (
                self.colors_settings['zodiac_radix_ring_2'])
            td['c2'] = 'class="circle" id="c2" cx="' + str(r) + '" cy="' + \
                str(r) + '" r="' + str(r-self.c2) + '"'
            td['c2style'] = 'fill: %s; fill-opacity: 1; stroke: %s; stroke-opacity:.4; stroke-width: 1px' % (
                self.colors_settings['paper_1'], self.colors_settings['zodiac_radix_ring_1'])
            td['c3'] = 'class="circle" id="c3" cx="' + str(r) + '" cy="' + \
                str(r) + '" r="' + str(r-self.c3) + '"'
            td['c3style'] = 'fill: %s; fill-opacity: 1; stroke: %s; stroke-width: 1px' % (
                self.colors_settings['paper_1'], self.colors_settings['zodiac_radix_ring_0'])
            td['c4'] = 'class="circle" id="c4" cx="' + str(r) + '" cy="' + \
                str(r) + '" r="' + str(r-self.c4) + '"'
            td['c4style'] = 'fill: %s; fill-opacity: 1; stroke: %s; stroke-width: 1px' % (
                self.colors_settings['paper_1'], self.colors_settings['zodiac_radix_ring_2'])
            td['makeAspects'] = self.__makeAspects(r, (r-self.c4))
            td['makeAxis'] = self.__makeAxis(r, (r-self.c1+30), self.user.axis_list, 8.4, '#ff0000', False)
            td['makeAspectGrid'] = self.__makeAspectGrid(r)
            td['makePatterns'] = self.__makePatterns()
            td['chart_width'] = self.natal_width

        td['circleX'] = str(0)
        td['circleY'] = str(0)
        td['svgWidth'] = str(svgWidth)
        td['svgHeight'] = str(svgHeight)
        td['viewbox'] = viewbox
        if self.chart_type == "Composite":
            td['stringTitle'] = f"{self.name} {self.language_settings['&']} {self.t_user.name}"
        elif self.chart_type == "Transit":
            td['stringTitle'] = f"{self.language_settings['transits']} {self.t_user.day}/{self.t_user.month}/{self.t_user.year}"
        else:
            td['stringTitle'] = self.name

        # Tipo di carta
        if self.chart_type == "Composite" or self.name == "Transit":
            td['stringName'] = f"{self.name}:"
        else:
            td['stringName'] = f'{self.language_settings["info"]}:'

        # bottom left

        td['bottomLeft1'] = ''
        td['bottomLeft2'] = ''
        td['bottomLeft3'] = f'{self.language_settings.get("lunar_phase", "Lunar Phase")}: {self.language_settings.get("day", "Day")} {self.lunar_phase.get("moon_phase", "")}'
        td['bottomLeft4'] = ''

        # lunar phase
        deg = self.lunar_phase['degrees_between_s_m']

        if(deg < 90.0):
            maxr = deg
            if(deg > 80.0):
                maxr = maxr*maxr
            lfcx = 20.0+(deg/90.0)*(maxr+10.0)
            lfr = 10.0+(deg/90.0)*maxr
            lffg, lfbg = self.colors_settings["lunar_phase_0"], self.colors_settings["lunar_phase_1"]

        elif(deg < 180.0):
            maxr = 180.0-deg
            if(deg < 100.0):
                maxr = maxr*maxr
            lfcx = 20.0+((deg-90.0)/90.0*(maxr+10.0))-(maxr+10.0)
            lfr = 10.0+maxr-((deg-90.0)/90.0*maxr)
            lffg, lfbg = self.colors_settings["lunar_phase_1"], self.colors_settings["lunar_phase_0"]

        elif(deg < 270.0):
            maxr = deg-180.0
            if(deg > 260.0):
                maxr = maxr*maxr
            lfcx = 20.0+((deg-180.0)/90.0*(maxr+10.0))
            lfr = 10.0+((deg-180.0)/90.0*maxr)
            lffg, lfbg = self.colors_settings["lunar_phase_1"], self.colors_settings["lunar_phase_0"]

        elif(deg < 361):
            maxr = 360.0-deg
            if(deg < 280.0):
                maxr = maxr*maxr
            lfcx = 20.0+((deg-270.0)/90.0*(maxr+10.0))-(maxr+10.0)
            lfr = 10.0+maxr-((deg-270.0)/90.0*maxr)
            lffg, lfbg = self.colors_settings["lunar_phase_0"], self.colors_settings["lunar_phase_1"]

        td['lunar_phase_fg'] = lffg
        td['lunar_phase_bg'] = lfbg
        td['lunar_phase_cx'] = lfcx
        td['lunar_phase_r'] = lfr
        td['lunar_phase_outline'] = self.colors_settings["lunar_phase_2"]

        # rotation based on latitude
        td['lunar_phase_rotate'] = (-90.0-self.geolat)

        # stringlocation
        if len(self.location) > 35:
            split = self.location.split(",")
            if len(split) > 1:
                td['stringLocation'] = split[0]+", "+split[-1]
                if len(td['stringLocation']) > 35:
                    td['stringLocation'] = td['stringLocation'][:35]+"..."
            else:
                td['stringLocation'] = self.location[:35]+"..."
        else:
            td['stringLocation'] = self.location

        td['stringDateTime'] = f'{self.user.year}-{self.user.month}-{self.user.day} {self.user.hour:02d}:{self.user.minute:02d}'

        if self.chart_type == "Composite":
            td['stringLat'] = f'{self.t_user.name}: '
            td['stringLon'] = self.t_user.city
            td['stringPosition'] = f'{self.t_user.year}-{self.t_user.month}-{self.t_user.day} {self.t_user.hour:02d}:{self.t_user.minute:02d}'

        else:
            td['stringLat'] = "%s: %s" % (
                self.language_settings['latitude'], self.__lat2str(self.geolat))
            td['stringLon'] = "%s: %s" % (
                self.language_settings['longitude'], self.__lon2str(self.geolon))
            td['stringPosition'] = f"{self.language_settings['type']}: {self.charttype}"

        # paper_color_X
        td['paper_color_0'] = self.colors_settings["paper_0"]
        td['paper_color_1'] = self.colors_settings["paper_1"]

        # planets_color_X
        for i in range(len(self.planets_settings)):
            td['planets_color_%s' %
                (i)] = self.colors_settings["planet_%s" % (i)]

        # zodiac_color_X
        for i in range(12):
            td['zodiac_color_%s' %
                (i)] = self.colors_settings["zodiac_icon_%s" % (i)]

        # orb_color_X
        for i in range(len(self.aspects_settings)):
            td['orb_color_%s' % (self.aspects_settings[i]['degree'])] = self.colors_settings["aspect_%s" % (
                self.aspects_settings[i]['degree'])]

        # config
        td['cfgZoom'] = str(self.zoom)
        td['cfgRotate'] = rotate
        td['cfgTranslate'] = translate

        # functions
        td['makeZodiac'] = self.__makeZodiac(r)
        td['makeHouses'] = self.__makeHouses(r)
        td['makeDegrees'] = self.__makeDegrees(r)
        td['makePlanets'] = self.__makePlanets(r)
        td['makeElements'] = self.__makeElements(r)
        td['makePlanetGrid'] = self.__makePlanetGrid()
        td['makeHousesGrid'] = self.__makeHousesGrid()
        
        

        # read template
        with open(self.xml_svg, "r", encoding="utf-8", errors='ignore') as output_file:
            f = open(self.xml_svg)
            template = Template(f.read()).substitute(td)

        # return filename

        return template.replace("\"", "'")

    def makeSVG(self):
        """Prints out the SVG file in the specifide folder"""

        if not (self.template):
            self.template = self.makeTemplate()

        self.chartname = self.output_directory / \
            f'{self.name}{self.chart_type}Chart.svg'

        with open(self.chartname, "w", encoding='utf-8', errors='ignore') as output_file:
            output_file.write(self.template)

        return print(f"SVG Generated Correctly in: {self.chartname}")


if __name__ == "__main__":

    first = KrInstance("Jack", 1990, 6, 15, 15, 15, "Roma")
    second = KrInstance("Jane", 1991, 10, 25, 21, 00, "Roma")

    name = MakeSvgInstance(first, chart_type="Composite",
                           second_obj=second, lang="IT")
    # name.output_directory = Path.home() / "charts"
    template = name.makeTemplate()
    name.makeSVG()
    print(name.aspects_list[-1])
    name.makeSVG()
    print(template)