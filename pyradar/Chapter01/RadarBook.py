"""
Project: RadarBook
File: RadarBook.py
Created by: Lee A. Harrison
On: 4/4/2019
Created with: PyCharm
"""
import sys
from Chapter01.ui.RadarBook_ui import Ui_MainWindow
from Chapter02 import apparent_elevation_example, apparent_range_example, atmosphere_example, beam_spreading_example, \
    cloud_fog_example, diffraction_example, ducting_example, plane_waves_example, rain_attenuation_example, \
    reflection_transmission_example, vegetation_example
from Chapter03 import circular_array_example, circular_aperture_example, horn_example, linear_array_example, \
    linear_wire_example, loop_example, planar_array_example, rectangular_aperture_example
from Chapter04 import hertzian_dipole_example, loop_gain_example, maximum_detection_range_example, \
    minimum_detectable_signal_example, output_signal_to_noise_bistatic_example, output_signal_to_noise_example, \
    output_signal_to_noise_search_example, ovals_of_cassini_example, power_aperture_example, \
    power_at_radar_bistatic_example, power_at_radar_example, power_density_example
from Chapter05 import adc_example, coherent_detector_example, envelope_detector_example, low_pass_filter_example, \
    noise_figure_example, resolution_example, sensitivity_time_control_example
from Chapter06 import binary_integration_example, cfar_example, coherent_integration_example, gaussian_noise_pd_example, \
    non_coherent_integration_example, optimum_binary_example, probability_distributions_example, \
    rayleigh_noise_pd_example, shnidman_example, single_pulse_snr_example
from Chapter07 import fdtd_example, frustum_example, infinite_cylinder_example, infinite_cylinder_oblique_example, \
    infinite_strip_example, po_example, rectangular_plate_example, right_circular_cone_example, \
    rounded_nose_cone_example, stratified_sphere_example
from Chapter08 import barker_ambiguity_example, frank_ambiguity_example, lfm_train_ambiguity_example, \
    lfm_pulse_ambiguity_example, matched_filter_example, PRN_ambiguity_example, pulse_train_ambiguity_example, \
    single_pulse_ambiguity_example, stepped_frequency_example, stretch_processor_example
from Chapter09 import alpha_beta_example, alpha_beta_gamma_example, kalman_ca_example, kalman_cv_example, \
    kalman_epsilon_example, kalman_sigma_example
from Chapter10 import back_projection_example, back_projection_3d_example, back_projection_backhoe_example, \
    back_projection_cv_example, stripmap_example, stripmap_cv_example
from Chapter11 import burnthrough_range_example, crossover_range_example, delay_line_example, jammer_to_signal_example
from PyQt5.QtWidgets import QApplication, QMainWindow


class RadarBook(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the tool tree
        self.toolsTree.itemDoubleClicked.connect(self._run_tool)

    def _run_tool(self):
        """
        Run the user selected tool
        :return:
        """

        # Get the selected item
        item = self.toolsTree.currentItem()
        tool = item.text(0)

        # Run selected tool
        # Chapter 2
        if tool == 'Apparent Elevation':
            apparent_elevation_example.start()
        elif tool == 'Apparent Range':
            apparent_range_example.start(self)
        elif tool == 'Atmospheric Attenuation':
            atmosphere_example.start()
        elif tool == 'Beam Spreading':
            beam_spreading_example.start()
        elif tool == 'Cloud/Fog Attenuation':
            cloud_fog_example.start()
        elif tool == 'Diffraction':
            diffraction_example.start()
        elif tool == 'Ducting':
            ducting_example.start()
        elif tool == 'Plane Waves':
            plane_waves_example.start()
        elif tool == 'Rain Attenuation':
            rain_attenuation_example.start()
        elif tool == 'Reflection / Transmission':
            reflection_transmission_example.start()
        elif tool == 'Vegetation Attenuation':
            vegetation_example.start()

        # Chapter 3
        elif tool == 'Linear Wires':
            linear_wire_example.start()
        elif tool == 'Loop Antenna':
            loop_example.start()
        elif tool == 'Rectangular Aperture':
            rectangular_aperture_example.start()
        elif tool == 'Circular Aperture':
            circular_aperture_example.start()
        elif tool == 'Horn Antenna':
            horn_example.start()
        elif tool == 'Linear Array':
            linear_array_example.start()
        elif tool == 'Circular Array':
            circular_array_example.start()
        elif tool == 'Planar Array':
            planar_array_example.start()

        # Chapter 4
        elif tool == 'Hertzian Dipole':
            hertzian_dipole_example.start()
        elif tool == 'Loop Gain':
            loop_gain_example.start(self)
        elif tool == 'Maximum Detection Range':
            maximum_detection_range_example.start()
        elif tool == 'Minimum Detectable Signal':
            minimum_detectable_signal_example.start(self)
        elif tool == 'Output SNR Monostatic':
            output_signal_to_noise_example.start()
        elif tool == 'Output SNR Search':
            output_signal_to_noise_search_example.start()
        elif tool == 'Output SNR Bistatic':
            output_signal_to_noise_bistatic_example.start()
        elif tool == 'Ovals of Cassini':
            ovals_of_cassini_example.start()
        elif tool == 'Power Aperture':
            power_aperture_example.start()
        elif tool == 'Power at Radar Monostatic':
            power_at_radar_example.start()
        elif tool == 'Power at Radar Bistatic':
            power_at_radar_bistatic_example.start()
        elif tool == 'Power Density':
            power_density_example.start()

        # Chapter 5
        elif tool == 'Analog to Digital':
            adc_example.start()
        elif tool == 'Coherent Detector':
            coherent_detector_example.start()
        elif tool == 'Envelope Detector':
            envelope_detector_example.start()
        elif tool == 'Low Pass Filter':
            low_pass_filter_example.start()
        elif tool == 'Noise Figure':
            noise_figure_example.start(self)
        elif tool == 'ADC Resolution':
            resolution_example.start(self)
        elif tool == 'Sensitivity Time Control':
            sensitivity_time_control_example.start()

        # Chapter 6
        elif tool == 'Binary Integration':
            binary_integration_example.start()
        elif tool == 'Constant False Alarm Rate':
            cfar_example.start()
        elif tool == 'Coherent Integration':
            coherent_integration_example.start()
        elif tool == 'Gaussian Noise Pd':
            gaussian_noise_pd_example.start()
        elif tool == 'Non-Coherent Integration':
            non_coherent_integration_example.start()
        elif tool == 'Optimum Binary Integration':
            optimum_binary_example.start()
        elif tool == 'Probability Distributions':
            probability_distributions_example.start()
        elif tool == 'Rayleigh Noise Pd':
            rayleigh_noise_pd_example.start()
        elif tool == 'Shnidman Approximation':
            shnidman_example.start()
        elif tool == 'Single Pulse SNR':
            single_pulse_snr_example.start()

        # Chapter 7
        elif tool == 'Finite Difference Time Domain':
            fdtd_example.start()
        elif tool == 'Frustum':
            frustum_example.start()
        elif tool == 'Infinite Cylinder':
            infinite_cylinder_example.start()
        elif tool == 'Infinite Cylinder Oblique':
            infinite_cylinder_oblique_example.start()
        elif tool == 'Infinite Strip':
            infinite_strip_example.start()
        elif tool == 'Physical Optics':
            po_example.start()
        elif tool == 'Rectangular Plate':
            rectangular_plate_example.start()
        elif tool == 'Right Circular Cone':
            right_circular_cone_example.start()
        elif tool == 'Rounded Nose Cone':
            rounded_nose_cone_example.start()
        elif tool == 'Stratified Sphere':
            stratified_sphere_example.start()

        # Chapter 8
        elif tool == 'Stepped Frequency':
            stepped_frequency_example.start()
        elif tool == 'Matched Filter':
            matched_filter_example.start()
        elif tool == 'Stretch Processor':
            stretch_processor_example.start()
        elif tool == 'Single Pulse' :
            single_pulse_ambiguity_example.start()
        elif tool == 'Pulse Train':
            pulse_train_ambiguity_example.start()
        elif tool == 'LFM Pulse':
            lfm_pulse_ambiguity_example.start()
        elif tool == 'LFM Train':
            lfm_train_ambiguity_example.start()
        elif tool == 'Barker Codes':
            barker_ambiguity_example.start()
        elif tool == 'Frank Codes':
            frank_ambiguity_example.start()
        elif tool == 'PRN Codes':
            PRN_ambiguity_example.start()

        # Chapter 9
        elif tool == 'Alpha Beta':
            alpha_beta_example.start()
        elif tool == 'Alpha Beta Gamma':
            alpha_beta_gamma_example.start()
        elif tool == 'Kalman Constant Velocity':
            kalman_cv_example.start()
        elif tool == 'Kalman Constant Acceleration' :
            kalman_ca_example.start()
        elif tool == 'Kalman Adaptive (epsilon)':
            kalman_epsilon_example.start()
        elif tool == 'Kalman Adaptive (sigma)':
            kalman_sigma_example.start()

        # Chapter 10
        elif tool == 'Back Projection 2D Points':
            back_projection_example.start()
        elif tool == 'Back Projection 2D Vehicles':
            back_projection_cv_example.start()
        elif tool == 'Back Projection 3D Points':
            back_projection_3d_example.start()
        elif tool == 'Back Projection 3D Backhoe':
            back_projection_backhoe_example.start()
        elif tool == 'Stripmap 2D Points':
            stripmap_example.start()
        elif tool == 'Stripmap 2D Vehicles':
            stripmap_cv_example.start()

        # Chapter 11
        elif tool == 'Jammer to Signal':
            jammer_to_signal_example.start()
        elif tool == 'Burn Through Range':
            burnthrough_range_example.start()
        elif tool == 'Crossover Range':
            crossover_range_example.start()
        elif tool == 'Delay Line':
            delay_line_example.start()


def main():
    app = QApplication(sys.argv)    # A new instance of QApplication
    form = RadarBook()              # Set the form
    form.show()                     # Show the form
    app.exec_()                     # Execute the app


if __name__ == '__main__':
    main()
