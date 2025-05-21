% Knowledge Base: Each issue with a list of symptoms
symptoms(hard_drive_failure, [slow_performance, strange_noises, corrupted_files, boot_failure, disk_errors]).
symptoms(ram_problems, [frequent_crashes, blue_screen, random_restarts, freezing, memory_errors]).
symptoms(overheating, [random_shutdowns, system_freezes, fans_running_loudly, sluggish_performance, hot_exterior]).
symptoms(power_supply_failure, [random_restarts, failure_to_power_on, system_shutdowns, clicking_noises, burning_smell]).
symptoms(malware_infection, [slow_performance, pop_ups, browser_redirection, disabled_security, unknown_processes]).
symptoms(driver_corruption, [device_malfunction, blue_screen, device_not_recognized, graphical_glitches, audio_problems]).
symptoms(bios_corruption, [failure_to_boot, beep_codes, missing_hardware, settings_reset, incorrect_date_time]).
symptoms(network_card_failure, [intermittent_connectivity, no_internet_access, network_not_detected, slow_connection, driver_errors]).
symptoms(monitor_problems, [flickering_screen, no_display, distorted_colors, dead_pixels, vertical_lines]).
symptoms(keyboard_malfunction, [unresponsive_keys, stuck_keys, ghost_typing, delayed_response, keyboard_not_detected]).
symptoms(gpu_failure, [display_artifacts, screen_freezing, graphical_glitches, display_driver_crashes, blank_screen_with_system_running]).
symptoms(gpu_overheating, [graphics_stuttering, game_crashes, gpu_fan_running_loudly, performance_degradation_in_graphics, display_corruption_under_load]).
symptoms(gpu_driver_issues, [display_flickering, color_distortion, application_crashes_with_graphics, black_screen_after_driver_update, poor_3d_performance]).

% Count how many symptoms match
match_count([], _, 0).    
match_count([S|Rest], List, Count) :-   member(S, List),  match_count(Rest, List, Count1), Count is Count1 + 1.
match_count([S|Rest], List, Count) :- \+ member(S, List), match_count(Rest, List, Count).



diagnose_all(UserSymptoms, Results) :-findall(Issue, symptoms(Issue, _), AllIssues), findall( issue(Issue, Percentage),
        (
            member(Issue, AllIssues),
            symptoms(Issue, SymptomList),
            match_count(UserSymptoms, SymptomList, Count),
            Count > 0,
            length(SymptomList, Total),
            Percentage is Count / Total * 100
        ),
        Results
    ).


