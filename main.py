from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox
from pyswip import Prolog
from pyswip.easy import Functor

# This class is used to display the results of the diagnosis
class ResultsDialog(QDialog):
    def __init__(self, resultsText):
        super().__init__()
        uic.loadUi("results.ui", self)
        self.results_text.setPlainText(resultsText)

# This class is the main page of the application
class MainPage(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("mainpage.ui", self)

        self.prolog = Prolog()
        self.prolog.consult("info.pl")

        self.confirm_button.clicked.connect(self.run_diagnosis)

        # All Checkboxes Available
        self.symptom_checkboxes = [
            self.blue_screen,
            self.random_restarts,
            self.random_shutdowns,
            self.unknown_processes,
            self.device_not_recognized,
            self.settings_reset,
            self.driver_errors,
            self.black_screen_after_driver_update,
            self.display_driver_crashes,
            self.blank_screen_with_system_running,
            self.disabled_security,
            self.pop_ups,
            self.slow_performance,
            self.boot_failure,
            self.incorrect_date_time,
            self.beep_codes,
            self.strange_noises,
            self.hot_exterior,
            self.clicking_noises,
            self.audio_problems,
            self.missing_hardware,
            self.gpu_fan_running_loudly,
            self.memory_errors,
            self.device_malfunction,
            self.disk_errors,
            self.corrupted_files,
            self.display_artifacts,
            self.graphical_glitches,
            self.flickering_screen,
            self.no_display,
            self.distorted_colors,
            self.dead_pixels,
            self.vertical_lines,
            self.intermittent_connectivity,
            self.no_internet_access,
            self.network_not_detected,
            self.slow_connection,
            self.browser_redirection,
            self.unresponsive_keys,
            self.stuck_keys,
            self.ghost_typing,
            self.delayed_response,
            self.keyboard_not_detected,
            self.freezing,
            self.frequent_crashes,
            self.poor_3d_performance,
            self.application_crashes_with_graphics,
            self.game_crashes
        ]
            # self.system_freezes,
            # self.fans_running_loudly,
            # self.sluggish_performance,
            # self.failure_to_power_on,
            # self.system_shutdowns,
            # self.burning_smell,
            # self.failure_to_boot,
            # self.screen_freezing,
            # self.graphics_stuttering,
            # self.performance_degradation_in_graphics,
            # self.display_corruption_under_load,
            # self.display_flickering,
            # self.color_distortion,

    
        
    # Get the checked symptoms and add them to checked list
    def get_checked_symptoms(self):
        checked = []
        for cb in self.symptom_checkboxes:
            if cb.isChecked():
                symptom = cb.text().lower().replace(" ", "_")
                checked.append(symptom)
        return checked

    # Run the diagnosis based on the selected symptoms (Prolog query)
    def run_diagnosis(self):
        selected = self.get_checked_symptoms()

        # Check if at least five symptoms are selected  ?? (or should i make it only one?)
        if len(selected) < 5:
            QMessageBox.warning(self, "Not Enough Symptoms Selected", "Please select at least five symptom.")
            return

        symptom_list_str = "[" + ",".join(selected) + "]"
        query = f"diagnose_all({symptom_list_str}, Results)."

        try:
            result = list(self.prolog.query(query))
            if not result:
                results_text = "No matching issue found."
            else:
                results = result[0]['Results']
                # print("Prolog Results Raw:", results)

                results_text = ""

                ##### Don't know how to aproach this yet #####

                # for issue in results:
                #     if hasattr(issue, 'args') and len(issue.args) == 2:
                #         name = str(issue.args[0])
                #         percentage = float(issue.args[1])
                #         results_text += f"{name}: {percentage:.2f}% match\n"
                #     else:
                #         results_text += f"Unrecognized format: {issue}\n"

            # dialog = ResultsDialog(results_text)
            # dialog.exec_()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication([])
    window = MainPage()
    window.show()
    app.exec_()
