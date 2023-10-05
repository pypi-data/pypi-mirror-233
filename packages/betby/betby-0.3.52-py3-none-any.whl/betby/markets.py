import numpy as np
from math import exp, factorial
import markets
from markets.specifiers import format_specifiers

markets_list = [
    {'market_id': '1',
     'market_name': 'THREE_WAY_WINNER',
     'market_outcomes': ['THREE_WAY_WINNER_HOME',
                         'THREE_WAY_WINNER_DRAW',
                         'THREE_WAY_WINNER_AWAY']},
    {'market_id': '10',
     'market_name': 'DOUBLE_CHANCE',
     'market_outcomes': ['DOUBLE_CHANCE_HOME_DRAW',
                         'DOUBLE_CHANCE_HOME_AWAY',
                         'DOUBLE_CHANCE_DRAW_AWAY']},
    {'market_id': '29',
     'market_name': 'BOTH_TO_SCORE',
     'market_outcomes': ['BOTH_TO_SCORE_YES',
                         'BOTH_TO_SCORE_NO']},
    {'market_id': '16',
     'market_name': 'HANDICAP',
     'market_outcomes': ['HANDICAP_HOME',
                         'HANDICAP_AWAY']},
    {'market_id': '50056',
     'market_name': 'MATCH_REST_HANDICAP',
     'market_outcomes': ['MATCH_REST_HANDICAP_HOME',
                         'MATCH_REST_HANDICAP_AWAY']},
    {'market_id': '18',
     'market_name': 'TOTAL',
     'market_outcomes': ['TOTAL_OVER',
                         'TOTAL_UNDER']},
    {'market_id': '19',
     'market_name': 'HOME_TOTAL',
     'market_outcomes': ['HOME_TOTAL_OVER',
                         'HOME_TOTAL_UNDER']},
    {'market_id': '20',
     'market_name': 'AWAY_TOTAL',
     'market_outcomes': ['AWAY_TOTAL_OVER',
                         'AWAY_TOTAL_UNDER']},
    {'market_id': '60',
     'market_name': 'FIRST_HALF_THREE_WAY_WINNER',
     'market_outcomes': ['FIRST_HALF_THREE_WAY_WINNER_HOME',
                         'FIRST_HALF_THREE_WAY_WINNER_DRAW',
                         'FIRST_HALF_THREE_WAY_WINNER_AWAY']},
    {'market_id': '63',
     'market_name': 'FIRST_HALF_DOUBLE_CHANCE',
     'market_outcomes': ['FIRST_HALF_DOUBLE_CHANCE_HOME_DRAW',
                         'FIRST_HALF_DOUBLE_CHANCE_HOME_AWAY',
                         'FIRST_HALF_DOUBLE_CHANCE_DRAW_AWAY']},
    {'market_id': '75',
     'market_name': 'FIRST_HALF_BOTH_TO_SCORE',
     'market_outcomes': ['FIRST_HALF_BOTH_TO_SCORE_YES',
                         'FIRST_HALF_BOTH_TO_SCORE_NO']},
    {'market_id': '66',
     'market_name': 'FIRST_HALF_HANDICAP',
     'market_outcomes': ['FIRST_HALF_HANDICAP_HOME',
                         'FIRST_HALF_HANDICAP_AWAY']},
    {'market_id': '50058',
     'market_name': 'FIRST_HALF_REST_HANDICAP',
     'market_outcomes': ['FIRST_HALF_REST_HANDICAP_HOME',
                         'FIRST_HALF_REST_HANDICAP_AWAY']},
    {'market_id': '68',
     'market_name': 'FIRST_HALF_TOTAL',
     'market_outcomes': ['FIRST_HALF_TOTAL_OVER',
                         'FIRST_HALF_TOTAL_UNDER']},
    {'market_id': '69',
     'market_name': 'FIRST_HALF_HOME_TOTAL',
     'market_outcomes': ['FIRST_HALF_HOME_TOTAL_OVER',
                         'FIRST_HALF_HOME_TOTAL_UNDER']},
    {'market_id': '70',
     'market_name': 'FIRST_HALF_AWAY_TOTAL',
     'market_outcomes': ['FIRST_HALF_AWAY_TOTAL_OVER',
                         'FIRST_HALF_AWAY_TOTAL_UNDER']},
]

class Get_markets:
    def __init__(self, avg_1, avg_2, score_1=0, score_2=0, time=0,
                 time_full=93, time_block=90, time_block_asian=90,
                 matrix=None, poisson=False, result=None):
        self.avg_1 = avg_1
        self.avg_2 = avg_2
        self.score_1 = score_1
        self.score_2 = score_2
        self.time = time
        self.time_full = time_full
        self.time_block = time_block
        self.time_block_asian = time_block_asian
        self.matrix = matrix
        self.poisson = poisson
        self.result = {} if result is None else result
        self.poi_1 = len(matrix[0]) if not poisson else None
        self.betstop = 0
        self.betstop_asian = 0
        if self.time > self.time_block:
            self.betstop = 1
        if self.time > self.time_block_asian:
            self.betstop_asian = 1

    # округление кэфов
    def kf_round(self, a, max):
        if a < 3.5:
            a = np.floor(a * 100) / 100
        elif a < 10:
            a = np.floor(a * 10) / 10
        elif a < max:
            a = np.floor(a)
        else:
            a = max
        if a > max:
            a = max
        return a

    # расчет маржи, кэфы на победу низкие
    def margin(self, kf, m=0.05, max=25):

        k_0 = 22 * 0.045 / m  # убывающая прямая
        v_0 = (-m + 0.23 - 0.5 / k_0) / (0.23 - 1 / k_0)  # предельная вер
        m_0 = 0.23 * (1 - v_0)
        n_0 = (1.5 - 1 / k_0) / (1.5 - 0.23)  # показатель (производная)
        ver = 0.5 + abs(1 / kf - 0.5)
        mar_1 = m - (ver - 0.5) / k_0
        mar_2 = 1.5 * (1 - ver) - (1.5 - 0.23) * (
                1 - v_0) * ((1 - ver) / (1 - v_0)) ** n_0
        if ver >= v_0:
            kf_v = (1 - mar_2) / ver
        else:
            kf_v = (1 - mar_1) / ver
        if 1 / kf >= 0.5:
            kf = self.kf_round(kf_v, max)
        else:
            kf = self.kf_round((1 - m) * kf_v / (kf_v - 1 + m), max)
        return kf

    def get_outcome(self, *factor):
        '''

        :param factor:
        :return: correct type of data
        '''
        if factor is None:
            return {'k': '0.0', 'b': 1}
        k, b = factor
        return {
            'k': str(k),
            'b': b,
        }

    def asian_spec(self, prob_a, prob_b, s=0):
        '''

        :param prob_a: prob of win spec
        :param prob_b: prob of win spec +-1
        :param s: asian or whole
        :return: prob = 1 / odds
        '''
        asian_prob = 0
        if s == 0:
            asian_prob = 1 / ((
                    1 - max(prob_a, prob_b)) / min(prob_a, prob_b) + 1)
        if s == 0.75:
            asian_prob = 2 * min(prob_a, prob_b) / (
                    2 - max(prob_a, prob_b) + min(prob_a, prob_b))
        if s == 0.25:
            asian_prob = (min(prob_a, prob_b) + max(prob_a, prob_b)) / (
                    2 - max(prob_a, prob_b) + min(prob_a, prob_b))
        return asian_prob

    def get_matrix(self):
        avg_1 = self.avg_1 * (self.time_full - self.time) / self.time_full
        avg_2 = self.avg_2 * (self.time_full - self.time) / self.time_full
        if self.poisson:
            self.matrix = np.zeros((self.poisson, self.poisson))
            for i in range(self.poisson):
                for j in range(self.poisson):
                    prob = (exp(-avg_1) * avg_1 ** i / factorial(i)) * (
                            exp(-avg_2) * avg_2 ** j / factorial(j))
                    self.matrix[i, j] = prob
        return self.matrix

    def two_way(self, mar=0.05, min_prob=0.02, max_odds=25, prob_tw=0,
                market_bl=0, market_id=None):
        '''

        :param mar:
        :param min_prob:
        :param max_odds:
        :param prob_tw:
        :param market_id:
        :return:
        '''
        self.market_id = market_id
        self.mar = mar
        self.min_prob = min_prob
        self.max_odds = max_odds
        self.prob_tw = prob_tw
        self.market_bl = market_bl
        self.odd_1 = 1
        self.odd_2 = 1
        matching_market = [market for market in markets_list if
                           market['market_id'] == self.market_id]
        market_name = matching_market[0]['market_name']
        market_outcomes = matching_market[0]['market_outcomes']

        if self.prob_tw < 0.999 and self.prob_tw > 0.001:
            self.odd_1 = self.margin(1 / self.prob_tw, self.mar, self.max_odds)
            self.odd_2 = self.margin(
                1 / (1 - self.prob_tw), self.mar, self.max_odds)
        if self.prob_tw < self.min_prob or self.prob_tw > 1 - self.min_prob:
            self.market_bl = 1

        new_data = {
            getattr(markets, market_name): {
                format_specifiers(getattr(markets, market_name), {}): {
                    getattr(markets, market_outcomes[0]): self.get_outcome(
                        self.odd_1, self.market_bl),
                    getattr(markets, market_outcomes[1]): self.get_outcome(
                        self.odd_2, self.market_bl),
                } if not self.market_bl + self.betstop else {},
            },
        }
        self.result = {**self.result, **new_data}

    def winner_3_way(self, mar=0.05, min_prob=0.02, max_odds=250,
                     market_bl=0, market_id=None):
        '''

        :param mar:
        :param min_prob:
        :param max_odds:
        :param market_id:
        :return:
        '''
        self.market_id = market_id
        self.mar = mar
        self.min_prob = min_prob
        self.max_odds = max_odds
        self.market_bl = market_bl
        prob_1 = 0
        prob_2 = 0

        matching_market = [market for market in markets_list if
                           market['market_id'] == self.market_id]
        market_name = matching_market[0]['market_name']
        market_outcomes = matching_market[0]['market_outcomes']

        for i in range(self.poisson or self.poi_1):
            for j in range(self.poisson or self.poi_1):
                if j - i < -0.5 + self.score_1 - self.score_2:
                    prob_1 += self.matrix[i, j]
                if j - i > 0.5 + self.score_1 - self.score_2:
                    prob_2 += self.matrix[i, j]
        hand_key = format_specifiers(getattr(markets, market_name), {})
        hand_dict = {}

        if prob_1 > 0 and prob_2 > 0 and 1 - prob_1 - prob_2 > 0 and \
                prob_1 < 1 and prob_2 < 1 and 1 - prob_1 - prob_2 < 1:
            hand_dict = {
                getattr(markets, market_outcomes[0]): self.get_outcome(
                    self.margin(
                        1 / prob_1, self.mar, self.max_odds), self.market_bl),
                getattr(markets, market_outcomes[1]): self.get_outcome(
                    self.margin(1 / (
                            1 - prob_1 - prob_2), self.mar, self.max_odds),
                    self.market_bl),
                getattr(markets, market_outcomes[2]): self.get_outcome(
                    self.margin(
                        1 / prob_2, self.mar, self.max_odds), self.market_bl)
            }
        if (
            not self.betstop
            and not self.market_bl
            and prob_1 <= 1 - self.min_prob
            and prob_1 >= self.min_prob
            and prob_2 <= 1 - self.min_prob
            and prob_2 >= self.min_prob
            and 1 - prob_1 - prob_2 <= 1 - self.min_prob
            and 1 - prob_1 - prob_2 >= self.min_prob
            and hand_dict
        ):
            if getattr(markets, market_name) not in self.result:
                self.result[getattr(markets, market_name)] = {}
            self.result[
                getattr(markets, market_name)].update({hand_key: hand_dict})

    def double_chance(self, mar=0.05, min_prob=0.02, max_odds=25,
                     market_bl=0, market_id=None):
        '''

        :param mar:
        :param min_prob:
        :param max_odds:
        :param market_bl:
        :param market_id:
        :return:
        '''
        self.market_id = market_id
        self.mar = mar
        self.min_prob = min_prob
        self.max_odds = max_odds
        self.market_bl = market_bl

        matching_market = [market for market in markets_list if
                           market['market_id'] == self.market_id]
        market_name = matching_market[0]['market_name']
        market_outcomes = matching_market[0]['market_outcomes']

        prob_1 = 0
        prob_2 = 0
        for i in range(self.poisson or self.poi_1):
            for j in range(self.poisson or self.poi_1):
                if j - i < 0.5 + self.score_1 - self.score_2:
                    prob_1 += self.matrix[i, j]
                if j - i > -0.5 + self.score_1 - self.score_2:
                    prob_2 += self.matrix[i, j]
        hand_key = format_specifiers(getattr(markets, market_name), {})
        hand_dict = {}

        if prob_1 > 0 and prob_2 > 0 and 2 - prob_1 - prob_2 > 0 and \
                prob_1 < 1 and prob_2 < 1 and 2 - prob_1 - prob_2 < 1:
            hand_dict = {
                getattr(markets, market_outcomes[0]): self.get_outcome(
                    self.margin(
                        1 / prob_1, self.mar, self.max_odds), self.market_bl),
                getattr(markets, market_outcomes[1]): self.get_outcome(
                    self.margin(1 / (
                            2 - prob_1 - prob_2), self.mar, self.max_odds),
                    self.market_bl),
                getattr(markets, market_outcomes[2]): self.get_outcome(
                    self.margin(
                        1 / prob_2, self.mar, self.max_odds), self.market_bl)
            }
        if (
            not self.betstop
            and not self.market_bl
            and prob_1 <= 1 - self.min_prob
            and prob_1 >= self.min_prob
            and prob_2 <= 1 - self.min_prob
            and prob_2 >= self.min_prob
            and 2 - prob_1 - prob_2 <= 1 - self.min_prob
            and 2 - prob_1 - prob_2 >= self.min_prob
            and hand_dict
        ):
            if getattr(markets, market_name) not in self.result:
                self.result[getattr(markets, market_name)] = {}
            self.result[getattr(markets, market_name)].update(
                {hand_key: hand_dict})

    def total(self, mar=0.05, min_prob=0.2, max_odds=25, asian=False,
                     market_bl=0, market_id=None):
        '''

        :param mar:
        :param min_prob:
        :param max_odds:
        :param asian:
        :param market_bl:
        :param market_id:
        :return:
        '''
        self.market_id = market_id
        self.mar = mar
        self.min_prob = min_prob
        self.max_odds = max_odds
        self.asian = asian
        self.market_bl = market_bl

        matching_market = [market for market in markets_list if
                           market['market_id'] == self.market_id]
        market_name = matching_market[0]['market_name']
        market_outcomes = matching_market[0]['market_outcomes']

        prob = 0
        prob_1 = 0
        for val in range(2 * self.poisson or 2 * self.poi_1):
            for i in range(self.poisson or self.poi_1):
                for j in range(self.poisson or self.poi_1):
                    if i + j < val + 0.5:
                        prob += self.matrix[i, j]
            total_key = format_specifiers(getattr(markets, market_name), {
                'total': str(val + 0.5 + self.score_1 + self.score_2)})
            total_dict = {}

            if prob > 0 and prob < 1:
                total_dict = {
                    getattr(markets, market_outcomes[0]): self.get_outcome(
                        self.margin(
                            1 / (1 - prob), self.mar, self.max_odds),
                        self.market_bl),
                    getattr(markets, market_outcomes[1]): self.get_outcome(
                        self.margin(
                            1 / prob, self.mar, self.max_odds), self.market_bl)
                }

            if prob > 0 and prob < 1 and prob_1 > 0 and prob_1 < 1 and asian:

                prob_asian = self.asian_spec(prob, prob_1)
                prob_asian_0_75 = self.asian_spec(prob, prob_1, s=0.75)
                prob_asian_0_25 = self.asian_spec(prob, prob_1, s=0.25)

                total_key_asian = format_specifiers(
                    getattr(markets, market_name), {'total': str(
                        val + self.score_1 + self.score_2)})
                total_key_asian_0_75 = format_specifiers(getattr(
                    markets, market_name), {'total': str(
                    val - 0.25 + self.score_1 + self.score_2)})
                total_key_asian_0_25 = format_specifiers(getattr(
                    markets, market_name), {'total': str(
                    val + 0.25 + self.score_1 + self.score_2)})
                total_dict_asian = {
                    getattr(markets, market_outcomes[0]): self.get_outcome(
                        self.margin(
                            1 / (1 - prob_asian), self.mar, self.max_odds),
                        self.market_bl),
                    getattr(markets, market_outcomes[1]): self.get_outcome(
                        self.margin(
                            1 / prob_asian, self.mar, self.max_odds),
                        self.market_bl)
                }
                total_dict_asian_0_75 = {
                    getattr(markets, market_outcomes[0]): self.get_outcome(
                        self.margin(
                            1 / (1 - prob_asian_0_75), self.mar,
                            self.max_odds), self.market_bl),
                    getattr(markets, market_outcomes[1]): self.get_outcome(
                        self.margin(
                            1 / prob_asian_0_75, self.mar, self.max_odds),
                        self.market_bl)
                }
                total_dict_asian_0_25 = {
                    getattr(markets, market_outcomes[0]): self.get_outcome(
                        self.margin(
                            1 / (1 - prob_asian_0_25), self.mar,
                            self.max_odds), self.market_bl),
                    getattr(markets, market_outcomes[1]): self.get_outcome(
                        self.margin(
                            1 / prob_asian_0_25, self.mar, self.max_odds),
                        self.market_bl)
                }

                if not self.betstop and not self.betstop_asian and \
                        prob_asian_0_75 \
                        <= 1 - min_prob and prob_asian_0_75 >= min_prob and \
                        total_dict_asian_0_75:
                    if getattr(markets, market_name) not in self.result:
                        self.result[getattr(markets, market_name)] = {}
                    self.result[getattr(markets, market_name)].update({
                        total_key_asian_0_75: total_dict_asian_0_75})

                if not self.betstop and not self.betstop_asian and prob_asian \
                        <= 1 - min_prob and prob_asian >= min_prob and \
                        total_dict_asian:
                    if getattr(markets, market_name) not in self.result:
                        self.result[getattr(markets, market_name)] = {}
                    self.result[getattr(markets, market_name)].update({
                        total_key_asian: total_dict_asian})

                if not self.betstop and not self.betstop_asian and \
                        prob_asian_0_25 \
                        <= 1 - min_prob and prob_asian_0_25 >= min_prob and \
                        total_dict_asian_0_25:
                    if getattr(markets, market_name) not in self.result:
                        self.result[getattr(markets, market_name)] = {}
                    self.result[getattr(markets, market_name)].update({
                        total_key_asian_0_25: total_dict_asian_0_25})

            if not self.betstop and not self.market_bl and prob <= 1 - \
                    min_prob and prob >= min_prob and total_dict:
                if getattr(markets, market_name) not in self.result:
                    self.result[getattr(markets, market_name)] = {}
                self.result[getattr(markets, market_name)].update(
                    {total_key: total_dict})

            prob_1 = prob
            prob = 0

    def handicap(self, mar=0.05, min_prob=0.2, max_odds=25, asian=False,
                     market_bl=0, market_id=None):
        '''

        :param mar:
        :param min_prob:
        :param max_odds:
        :param asian:
        :param market_bl:
        :param market_id:
        :return:
        '''
        self.market_id = market_id
        self.mar = mar
        self.min_prob = min_prob
        self.max_odds = max_odds
        self.asian = asian
        self.market_bl = market_bl

        matching_market = [market for market in markets_list if
                           market['market_id'] == self.market_id]
        market_name = matching_market[0]['market_name']
        market_outcomes = matching_market[0]['market_outcomes']

        prob = 0
        prob_1 = 0
        for val in range(1 - (self.poisson or self.poi_1),
                         (self.poisson or self.poi_1) - 1):
            for i in range(self.poisson or self.poi_1):
                for j in range(self.poisson or self.poi_1):
                    if j - i > val + 0.5:
                        prob += self.matrix[i, j]
                        # print(val + 0.5, i, j, prob)
            hand_key = format_specifiers(getattr(markets, market_name), {
                'hcp': str(val + 0.5 - self.score_1 + self.score_2)})
            hand_dict = {}

            if prob > 0 and prob < 1:
                hand_dict = {
                    getattr(markets, market_outcomes[0]): self.get_outcome(
                        self.margin(1 / (
                        1 - prob), self.mar, self.max_odds), self.market_bl),
                    getattr(markets, market_outcomes[1]): self.get_outcome(
                        self.margin(
                        1 / prob, self.mar, self.max_odds), self.market_bl)
                }

            if prob > 0 and prob < 1 and prob_1 > 0 and prob_1 < 1 and asian:

                prob_asian = self.asian_spec(prob, prob_1)
                prob_asian_0_75 = self.asian_spec(prob, prob_1, s=0.75)
                prob_asian_0_25 = self.asian_spec(prob, prob_1, s=0.25)

                hand_key_asian = format_specifiers(
                    getattr(markets, market_name), {'hcp': str(
                        val - self.score_1 + self.score_2)})
                hand_key_asian_0_75 = format_specifiers(
                    getattr(markets, market_name), {'hcp': str(
                        val + 0.25 - self.score_1 + self.score_2)})
                hand_key_asian_0_25 = format_specifiers(
                    getattr(markets, market_name), {'hcp': str(
                        val - 0.25 - self.score_1 + self.score_2)})
                hand_dict_asian = {
                    getattr(markets, market_outcomes[0]): self.get_outcome(
                        self.margin(1 / (1 - prob_asian), self.mar,
                                    self.max_odds), self.market_bl),
                    getattr(markets, market_outcomes[1]): self.get_outcome(
                        self.margin(
                    1 / prob_asian, self.mar, self.max_odds), self.market_bl)
                }
                hand_dict_asian_0_75 = {
                    getattr(markets, market_outcomes[0]): self.get_outcome(
                        self.margin(1 / (1 - prob_asian_0_75), self.mar,
                                    self.max_odds), self.market_bl),
                    getattr(markets, market_outcomes[1]): self.get_outcome(
                        self.margin(1 / prob_asian_0_75, self.mar,
                                    self.max_odds), self.market_bl)
                }
                hand_dict_asian_0_25 = {
                    getattr(markets, market_outcomes[0]): self.get_outcome(
                        self.margin(1 / (1 - prob_asian_0_25), self.mar,
                                    self.max_odds), self.market_bl),
                    getattr(markets, market_outcomes[1]): self.get_outcome(
                        self.margin(1 / prob_asian_0_25, self.mar,
                                    self.max_odds), self.market_bl)
                }
                if not self.betstop and not self.betstop_asian and \
                        prob_asian_0_25 \
                        <= 1 - min_prob and prob_asian_0_25 >= min_prob and \
                        hand_dict_asian_0_25:
                    if getattr(markets, market_name) not in self.result:
                        self.result[getattr(markets, market_name)] = {}
                    self.result[getattr(markets, market_name)].update({
                        hand_key_asian_0_25: hand_dict_asian_0_25})

                if not self.betstop and not self.betstop_asian and prob_asian \
                        <= 1 - min_prob and prob_asian >= min_prob and \
                        hand_dict_asian:
                    if getattr(markets, market_name) not in self.result:
                        self.result[getattr(markets, market_name)] = {}
                    self.result[getattr(markets, market_name)].update({
                        hand_key_asian: hand_dict_asian})

                if not self.betstop and not self.betstop_asian and \
                        prob_asian_0_75 \
                        <= 1 - min_prob and prob_asian_0_75 >= min_prob and \
                        hand_dict_asian_0_75:
                    if getattr(markets, market_name) not in self.result:
                        self.result[getattr(markets, market_name)] = {}
                    self.result[getattr(markets, market_name)].update({
                        hand_key_asian_0_75: hand_dict_asian_0_75})

            if not self.betstop and not self.market_bl and prob <= 1 - \
                    min_prob and prob >= min_prob and hand_dict:
                if getattr(markets, market_name) not in self.result:
                    self.result[getattr(markets, market_name)] = {}
                self.result[getattr(markets, market_name)].update(
                    {hand_key: hand_dict})

            prob_1 = prob
            prob = 0

    def match_rest_handicap(self, mar=0.05, min_prob=0.2, max_odds=25,
                            asian=False, market_bl=0, market_id=None):
        '''

        :param mar:
        :param min_prob:
        :param max_odds:
        :param asian:
        :param market_bl:
        :param market_id:
        :return:
        '''
        self.market_id = market_id
        self.mar = mar
        self.min_prob = min_prob
        self.max_odds = max_odds
        self.asian = asian
        self.market_bl = market_bl

        matching_market = [market for market in markets_list if
                           market['market_id'] == self.market_id]
        market_name = matching_market[0]['market_name']
        market_outcomes = matching_market[0]['market_outcomes']

        prob = 0
        prob_1 = 0
        for val in range(1 - (self.poisson or self.poi_1),
                         (self.poisson or self.poi_1) - 1):
            for i in range(self.poisson or self.poi_1):
                for j in range(self.poisson or self.poi_1):
                    if j - i > val + 0.5:
                        prob += self.matrix[i, j]
                        # print(val + 0.5, i, j, prob)
            hand_key = format_specifiers(getattr(markets, market_name), {
                'score': str(self.score_1) + ':' + str(self.score_2),
                    'hcp': str(val + 0.5)})
            hand_dict = {}

            if prob > 0 and prob < 1:
                hand_dict = {
                    getattr(markets, market_outcomes[0]): self.get_outcome(
                        self.margin(1 / (
                        1 - prob), self.mar, self.max_odds), self.market_bl),
                    getattr(markets, market_outcomes[1]): self.get_outcome(
                        self.margin(
                        1 / prob, self.mar, self.max_odds), self.market_bl)
                }

            if prob > 0 and prob < 1 and prob_1 > 0 and prob_1 < 1 and asian:

                prob_asian = self.asian_spec(prob, prob_1)
                prob_asian_0_75 = self.asian_spec(prob, prob_1, s=0.75)
                prob_asian_0_25 = self.asian_spec(prob, prob_1, s=0.25)

                hand_key_asian = format_specifiers(
                    getattr(markets, market_name), {
                        'score': str(self.score_1) + ':' + str(self.score_2),
                    'hcp': str(val)})
                hand_key_asian_0_75 = format_specifiers(
                    getattr(markets, market_name), {
                        'score': str(self.score_1) + ':' + str(self.score_2),
                    'hcp': str(val + 0.25)})
                hand_key_asian_0_25 = format_specifiers(
                    getattr(markets, market_name), {
                        'score': str(self.score_1) + ':' + str(self.score_2),
                    'hcp': str(val - 0.25)})
                hand_dict_asian = {
                    getattr(markets, market_outcomes[0]): self.get_outcome(
                        self.margin(1 / (1 - prob_asian), self.mar,
                                    self.max_odds), self.market_bl),
                    getattr(markets, market_outcomes[1]): self.get_outcome(
                        self.margin(1 / prob_asian, self.mar,
                                    self.max_odds), self.market_bl)
                }
                hand_dict_asian_0_75 = {
                    getattr(markets, market_outcomes[0]): self.get_outcome(
                        self.margin(1 / (1 - prob_asian_0_75), self.mar,
                                    self.max_odds), self.market_bl),
                    getattr(markets, market_outcomes[1]): self.get_outcome(
                        self.margin(1 / prob_asian_0_75, self.mar,
                                    self.max_odds), self.market_bl)
                }
                hand_dict_asian_0_25 = {
                    getattr(markets, market_outcomes[0]): self.get_outcome(
                        self.margin(1 / (1 - prob_asian_0_25), self.mar,
                                    self.max_odds), self.market_bl),
                    getattr(markets, market_outcomes[1]): self.get_outcome(
                        self.margin(1 / prob_asian_0_25, self.mar,
                                    self.max_odds), self.market_bl)
                }
                if not self.betstop and not self.betstop_asian and \
                        prob_asian_0_25 \
                        <= 1 - min_prob and prob_asian_0_25 >= min_prob and \
                        hand_dict_asian_0_25:
                    if getattr(markets, market_name) not in self.result:
                        self.result[getattr(markets, market_name)] = {}
                    self.result[getattr(markets, market_name)].update({
                        hand_key_asian_0_25: hand_dict_asian_0_25})

                if not self.betstop and not self.betstop_asian and prob_asian \
                        <= 1 - min_prob and prob_asian >= min_prob and \
                        hand_dict_asian:
                    if getattr(markets, market_name) not in self.result:
                        self.result[getattr(markets, market_name)] = {}
                    self.result[getattr(markets, market_name)].update({
                        hand_key_asian: hand_dict_asian})

                if not self.betstop and not self.betstop_asian and \
                        prob_asian_0_75 \
                        <= 1 - min_prob and prob_asian_0_75 >= min_prob and \
                        hand_dict_asian_0_75:
                    if getattr(markets, market_name) not in self.result:
                        self.result[getattr(markets, market_name)] = {}
                    self.result[getattr(markets, market_name)].update({
                        hand_key_asian_0_75: hand_dict_asian_0_75})

            if not self.betstop and not self.market_bl and prob <= 1 - \
                    min_prob and prob >= min_prob and hand_dict:
                if getattr(markets, market_name) not in self.result:
                    self.result[getattr(markets, market_name)] = {}
                self.result[
                    getattr(markets, market_name)].update(
                    {hand_key: hand_dict})

            prob_1 = prob
            prob = 0

    def home_total(self, mar=0.05, min_prob=0.2, max_odds=25, asian=False,
                     market_bl=0, market_id=None):
        '''

        :param mar:
        :param min_prob:
        :param max_odds:
        :param asian:
        :param market_bl:
        :param market_id:
        :return:
        '''
        self.market_id = market_id
        self.mar = mar
        self.min_prob = min_prob
        self.max_odds = max_odds
        self.asian = asian
        self.market_bl = market_bl

        matching_market = [market for market in markets_list if
                           market['market_id'] == self.market_id]
        market_name = matching_market[0]['market_name']
        market_outcomes = matching_market[0]['market_outcomes']

        prob = 0
        prob_1 = 0
        for val in range(self.poisson or self.poi_1):
            for i in range(self.poisson or self.poi_1):
                for j in range(self.poisson or self.poi_1):
                    if i < val + 0.5:
                        prob += self.matrix[i, j]
            home_total_key = format_specifiers(getattr(markets, market_name), {
                'total': str(val + 0.5 + self.score_1)})
            home_total_dict = {}

            if prob > 0 and prob < 1:
                home_total_dict = {
                    getattr(markets, market_outcomes[0]): self.get_outcome(
                        self.margin(1 / (1 - prob), self.mar,
                                    self.max_odds), self.market_bl),
                    getattr(markets, market_outcomes[1]): self.get_outcome(
                        self.margin(1 / prob, self.mar, self.max_odds),
                        self.market_bl)
                }

            if prob > 0 and prob < 1 and prob_1 > 0 and prob_1 < 1 and asian:

                prob_asian = self.asian_spec(prob, prob_1)
                prob_asian_0_75 = self.asian_spec(prob, prob_1, s=0.75)
                prob_asian_0_25 = self.asian_spec(prob, prob_1, s=0.25)

                total_key_asian = format_specifiers(getattr(
                    markets, market_name), {'total': str(val + self.score_1)})
                total_key_asian_0_75 = format_specifiers(
                    getattr(markets, market_name), {'total': str(
                        val - 0.25 + self.score_1)})
                total_key_asian_0_25 = format_specifiers(
                    getattr(markets, market_name), {'total': str(
                        val + 0.25 + self.score_1)})
                total_dict_asian = {
                    getattr(markets, market_outcomes[0]): self.get_outcome(
                        self.margin(1 / (1 - prob_asian), self.mar,
                                    self.max_odds), self.market_bl),
                    getattr(markets, market_outcomes[1]): self.get_outcome(
                        self.margin(1 / prob_asian, self.mar,
                                    self.max_odds), self.market_bl)
                }
                total_dict_asian_0_75 = {
                    getattr(markets, market_outcomes[0]): self.get_outcome(
                        self.margin(1 / (1 - prob_asian_0_75), self.mar,
                                    self.max_odds), self.market_bl),
                    getattr(markets, market_outcomes[1]): self.get_outcome(
                        self.margin(1 / prob_asian_0_75, self.mar,
                                    self.max_odds), self.market_bl)
                }
                total_dict_asian_0_25 = {
                    getattr(markets, market_outcomes[0]): self.get_outcome(
                        self.margin(1 / (1 - prob_asian_0_25), self.mar,
                                    self.max_odds), self.market_bl),
                    getattr(markets, market_outcomes[1]): self.get_outcome(
                        self.margin(1 / prob_asian_0_25, self.mar,
                                    self.max_odds), self.market_bl)
                }

                if not self.betstop and not self.betstop_asian and \
                        prob_asian_0_75 \
                        <= 1 - min_prob and prob_asian_0_75 >= min_prob and \
                        total_dict_asian_0_75:
                    if getattr(markets, market_name) not in self.result:
                        self.result[getattr(markets, market_name)] = {}
                    self.result[getattr(markets, market_name)].update({
                        total_key_asian_0_75: total_dict_asian_0_75})

                if not self.betstop and not self.betstop_asian and prob_asian \
                        <= 1 - min_prob and prob_asian >= min_prob and \
                        total_dict_asian:
                    if getattr(markets, market_name) not in self.result:
                        self.result[getattr(markets, market_name)] = {}
                    self.result[getattr(markets, market_name)].update({
                        total_key_asian: total_dict_asian})

                if not self.betstop and not self.betstop_asian and \
                        prob_asian_0_25 \
                        <= 1 - min_prob and prob_asian_0_25 >= min_prob and \
                        total_dict_asian_0_25:
                    if getattr(markets, market_name) not in self.result:
                        self.result[getattr(markets, market_name)] = {}
                    self.result[getattr(markets, market_name)].update({
                        total_key_asian_0_25: total_dict_asian_0_25})

            if not self.betstop and not self.market_bl and prob <= 1 - \
                    min_prob and prob >= min_prob and home_total_dict:
                if getattr(markets, market_name) not in self.result:
                    self.result[getattr(markets, market_name)] = {}
                self.result[getattr(markets, market_name)].update(
                    {home_total_key: home_total_dict})

            prob_1 = prob
            prob = 0

    def away_total(self, mar=0.05, min_prob=0.2, max_odds=25, asian=False,
                     market_bl=0, market_id=None):
        '''

        :param mar:
        :param min_prob:
        :param max_odds:
        :param asian:
        :param market_bl:
        :param market_id:
        :return:
        '''
        self.market_id = market_id
        self.mar = mar
        self.min_prob = min_prob
        self.max_odds = max_odds
        self.asian = asian
        self.market_bl = market_bl

        matching_market = [market for market in markets_list if
                           market['market_id'] == self.market_id]
        market_name = matching_market[0]['market_name']
        market_outcomes = matching_market[0]['market_outcomes']

        prob = 0
        prob_1 = 0
        for val in range(self.poisson or self.poi_1):
            for i in range(self.poisson or self.poi_1):
                for j in range(self.poisson or self.poi_1):
                    if j < val + 0.5:
                        prob += self.matrix[i, j]
            away_total_key = format_specifiers(getattr(markets, market_name), {
                'total': str(val + 0.5 + self.score_2)})
            away_total_dict = {}

            if prob > 0 and prob < 1:
                away_total_dict = {
                    getattr(markets, market_outcomes[0]): self.get_outcome(
                        self.margin(1 / (1 - prob), self.mar,
                                    self.max_odds), self.market_bl),
                    getattr(markets, market_outcomes[1]): self.get_outcome(
                        self.margin(1 / prob, self.mar, self.max_odds),
                        self.market_bl)
                }

            if prob > 0 and prob < 1 and prob_1 > 0 and prob_1 < 1 and asian:

                prob_asian = self.asian_spec(prob, prob_1)
                prob_asian_0_75 = self.asian_spec(prob, prob_1, s=0.75)
                prob_asian_0_25 = self.asian_spec(prob, prob_1, s=0.25)

                total_key_asian = format_specifiers(
                    getattr(markets, market_name), {'total': str(
                        val + self.score_2)})
                total_key_asian_0_75 = format_specifiers(
                    getattr(markets, market_name), {'total': str(
                        val - 0.25 + self.score_2)})
                total_key_asian_0_25 = format_specifiers(
                    getattr(markets, market_name), {'total': str(
                        val + 0.25 + self.score_2)})
                total_dict_asian = {
                    getattr(markets, market_outcomes[0]): self.get_outcome(
                        self.margin(1 / (1 - prob_asian), self.mar,
                                    self.max_odds), self.market_bl),
                    getattr(markets, market_outcomes[1]): self.get_outcome(
                        self.margin(1 / prob_asian, self.mar, self.max_odds),
                        self.market_bl)
                }
                total_dict_asian_0_75 = {
                    getattr(markets, market_outcomes[0]): self.get_outcome(
                        self.margin(1 / (1 - prob_asian_0_75), self.mar,
                                    self.max_odds), self.market_bl),
                    getattr(markets, market_outcomes[1]): self.get_outcome(
                        self.margin(1 / prob_asian_0_75, self.mar,
                                    self.max_odds), self.market_bl)
                }
                total_dict_asian_0_25 = {
                    getattr(markets, market_outcomes[0]): self.get_outcome(
                        self.margin(1 / (1 - prob_asian_0_25), self.mar,
                                    self.max_odds), self.market_bl),
                    getattr(markets, market_outcomes[1]): self.get_outcome(
                        self.margin(1 / prob_asian_0_25, self.mar,
                                    self.max_odds), self.market_bl)
                }

                if not self.betstop and not self.betstop_asian and \
                        prob_asian_0_75 \
                        <= 1 - min_prob and prob_asian_0_75 >= min_prob and \
                        total_dict_asian_0_75:
                    if getattr(markets, market_name) not in self.result:
                        self.result[getattr(markets, market_name)] = {}
                    self.result[getattr(markets, market_name)].update({
                        total_key_asian_0_75: total_dict_asian_0_75})

                if not self.betstop and not self.betstop_asian and prob_asian \
                        <= 1 - min_prob and prob_asian >= min_prob and \
                        total_dict_asian:
                    if getattr(markets, market_name) not in self.result:
                        self.result[getattr(markets, market_name)] = {}
                    self.result[getattr(markets, market_name)].update({
                        total_key_asian: total_dict_asian})

                if not self.betstop and not self.betstop_asian and \
                        prob_asian_0_25 \
                        <= 1 - min_prob and prob_asian_0_25 >= min_prob and \
                        total_dict_asian_0_25:
                    if getattr(markets, market_name) not in self.result:
                        self.result[getattr(markets, market_name)] = {}
                    self.result[getattr(markets, market_name)].update({
                        total_key_asian_0_25: total_dict_asian_0_25})

            if not self.betstop and not self.market_bl and prob <= 1 - \
                    min_prob and prob >= min_prob and away_total_dict:
                if getattr(markets, market_name) not in self.result:
                    self.result[getattr(markets, market_name)] = {}
                self.result[getattr(markets, market_name)].update(
                    {away_total_key: away_total_dict})

            prob_1 = prob
            prob = 0
