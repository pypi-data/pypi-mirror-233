import spike2py_reflex as s2pr
import pytest


def test_reflex_outcomes_hreflex_doubles_individual_reflexes(info_data_hreflex):
    info, data = info_data_hreflex
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate_for_individual_reflexes(section)
    assert section.reflexes['Fdi'].reflexes[0].reflex1.outcomes['mmax'].peak_to_peak == pytest.approx(-0.0006542747927399485)
    assert section.reflexes['Fdi'].reflexes[0].reflex1.outcomes['mmax'].area == pytest.approx(0.009029248457930177)
    assert section.reflexes['Fdi'].reflexes[0].reflex1.outcomes['hreflex'].onset == pytest.approx(0.015625)
    assert section.reflexes['Fdi'].reflexes[0].reflex2.outcomes['hreflex'].peak_to_peak == pytest.approx(0.008616540378246568)


def test_reflex_outcomes_ramp_doubles_individual_reflexes(info_data_ramp):
    info, data = info_data_ramp
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate_for_individual_reflexes(section)
    assert section.reflexes['Fdi'].reflexes[0].outcomes['mmax'].peak_to_peak == pytest.approx(0.0008818809505351101)
    assert section.reflexes['Fdi'].reflexes[0].outcomes['mmax'].area == pytest.approx(0.07461095444461116)
    assert section.reflexes['Fdi'].reflexes[0].outcomes['hreflex'].onset is None


def test_reflex_outcomes_mmax_doubles_individual_reflexes(info_data_mmax):
    info, data = info_data_mmax
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate_for_individual_reflexes(section)
    print(section.reflexes['Fdi'].reflexes[0].outcomes)
    assert section.reflexes['Fdi'].reflexes[0].outcomes['mmax'].peak_to_peak == pytest.approx(-0.0036865157257219843)
    assert section.reflexes['Fdi'].reflexes[0].outcomes['mmax'].area == pytest.approx(59.2717048344781)
    assert section.reflexes['Fdi'].reflexes[0].outcomes['hreflex'].onset == pytest.approx(0.014616935483870967)


def test_reflex_outcomes_hreflex_doubles_avg(info_data_hreflex):
    info, data = info_data_hreflex
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate_for_individual_reflexes(section)
    section = s2pr.outcomes.calculate_outcomes_of_avg(section)
    assert len(section.reflexes['Fdi'].avg_reflex1[19].waveform) == 109
    assert section.reflexes['Fdi'].avg_reflex1[19].outcomes[
               'mmax'].peak_to_peak == pytest.approx(-0.0025790729955973923)
    assert section.reflexes['Fdi'].avg_reflex2[19].outcomes[
               'mmax'].area == pytest.approx(0.0172215595901918)


def test_reflex_outcomes_ramp_singles_avg(info_data_ramp):
    info, data = info_data_ramp
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate_for_individual_reflexes(section)
    section = s2pr.outcomes.calculate_outcomes_of_avg(section)
    assert len(section.reflexes['Fdi'].avg_waveform) == 3
    assert len(section.reflexes['Fdi'].avg_waveform[10].waveform) == 90
    assert len(section.reflexes['Fdi'].avg_waveform[24].waveform) == 90
    assert section.reflexes['Fdi'].avg_waveform[10].outcomes['mmax'].peak_to_peak == pytest.approx(-0.005731800364989032)
    assert section.reflexes['Fdi'].avg_waveform[10].outcomes[
               'hreflex'].peak_to_peak == pytest.approx(-0.00744452232263654)



def test_reflex_outcomes_mmax_singles_avg(info_data_mmax):
    info, data = info_data_mmax
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate_for_individual_reflexes(section)
    section = s2pr.outcomes.calculate_outcomes_of_avg(section)
    assert len(section.reflexes['Fdi'].avg_waveform) == 1
    assert len(section.reflexes['Fdi'].avg_waveform[1].waveform) == 694
    assert section.reflexes['Fdi'].avg_waveform[1].outcomes['mmax'].peak_to_peak == pytest.approx(0.000937179558910316)
    assert section.reflexes['Fdi'].avg_waveform[1].outcomes[
               'hreflex'].peak_to_peak == pytest.approx(0.0007075028492035976)


def test_reflex_outcomes_hreflex_doubles_mean(info_data_hreflex):
    info, data = info_data_hreflex
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate_for_individual_reflexes(section)
    section = s2pr.outcomes.calculate_mean_outcomes(section)
    assert section.reflexes['Fdi'].mean_outcomes_reflex1['mmax'][19]['outcomes'].peak_to_peak == pytest.approx(-0.0028362263004474337)
    assert section.reflexes['Fdi'].mean_outcomes_reflex1['mmax'][19]['missing_outcomes'].peak_to_peak == 0
    assert section.reflexes['Fdi'].mean_outcomes_reflex1['mmax'][19][
        'missing_outcomes'].onset == 5
    assert section.reflexes['Fdi'].mean_outcomes_reflex1['mmax'][19][
        'present_outcomes'].onset == 2
    assert section.reflexes['Fdi'].mean_ratio['mmax'][19]['ratio'] == pytest.approx(1.7850417839694663)
    assert section.reflexes['Fdi'].mean_ratio['mmax'][19]['missing_ratio'] == 0
    assert section.reflexes['Fdi'].mean_ratio['mmax'][19]['present_ratio'] == 7


def test_reflex_outcomes_ramp_train_mean(info_data_ramp):
    info, data = info_data_ramp
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate_for_individual_reflexes(section)
    section = s2pr.outcomes.calculate_mean_outcomes(section)
    assert section.reflexes['Fdi'].mean_outcomes['mmax'][10]['outcomes'].peak_to_peak == pytest.approx(-0.005557504746610184)
    assert section.reflexes['Fdi'].mean_outcomes['mmax'][10]['missing_outcomes'].peak_to_peak == 0
    assert section.reflexes['Fdi'].mean_outcomes['mmax'][10]['missing_outcomes'].onset == 19
    assert section.reflexes['Fdi'].mean_outcomes['mmax'][24][
               'missing_outcomes'].peak_to_peak == 0


def test_reflex_outcomes_mmax_single_mean(info_data_mmax):
    info, data = info_data_mmax
    section = s2pr.reflexes.extract(info, data)
    section = s2pr.outcomes.calculate_for_individual_reflexes(section)
    section = s2pr.outcomes.calculate_mean_outcomes(section)
    assert section.reflexes['Fdi'].mean_outcomes['mmax'][1]['outcomes'].peak_to_peak == pytest.approx(-0.0001343032256506074)
    assert section.reflexes['Fdi'].mean_outcomes['hreflex'][1]['missing_outcomes'].peak_to_peak == 0


def test_reflex_outcomes_mmax_single_mean_second_muscle(info_data_mmax):
    info, data = info_data_mmax
    section = s2pr.reflexes.extract(info, data)
    section.reflexes['Adm'] = section.reflexes['Fdi']
    section = s2pr.outcomes.calculate_for_individual_reflexes(section)
    section = s2pr.outcomes.calculate_mean_outcomes(section)
    assert section.reflexes['Adm'].mean_outcomes['mmax'][1]['outcomes'].peak_to_peak == pytest.approx(-0.0001343032256506074)
    assert section.reflexes['Adm'].mean_outcomes['hreflex'][1]['missing_outcomes'].peak_to_peak == 0
