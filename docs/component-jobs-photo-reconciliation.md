# Component Jobs vs Photo Inventory Reconciliation

- Generated: 2026-05-01 00:28:55
- Source component jobs: `data/manual/component_jobs.csv`
- Source photo inventory: `data/manual/photo_inventory.csv`
- Output CSV: `data/manual/component_jobs_photo_reconciliation.csv`

## Status Summary

- `direct_photo_evidence`: 29
- `indirect_photo_evidence_only`: 0
- `no_photo_evidence`: 6

## Per-Component Results

| Component Job | Status | Direct | Indirect | Direct Components | Notes |
| --- | --- | ---: | ---: | --- | --- |
| `eps_vitz_control_wiring_and_safety` | `no_photo_evidence` | 0 | 0 | `-` | No explicit rule configured. |
| `eps_vitz_donor_column_and_mounts` | `no_photo_evidence` | 0 | 0 | `-` | No explicit rule configured. |
| `interior_dash_switch_fitup` | `no_photo_evidence` | 0 | 0 | `-` | No explicit rule configured. |
| `interior_diesel_cutoff_ignition_security` | `no_photo_evidence` | 0 | 0 | `-` | No explicit rule configured. |
| `suspension_upgrade_fitment_and_alignment` | `no_photo_evidence` | 0 | 0 | `-` | No explicit rule configured. |
| `suspension_upgrade_spec_and_kit_lock` | `no_photo_evidence` | 0 | 0 | `-` | No explicit rule configured. |
| `back_cabin` | `direct_photo_evidence` | 5 | 15 | `body_shell_with_doors_removed|dashboard_shell_and_cabin|rear_cargo_floor|rear_side_opening` | Rear cabin/body section is directly visible in multiple strip-down shots. |
| `back_doors` | `direct_photo_evidence` | 19 | 2 | `detached_body_panels_and_doors|detached_doors_and_panels` | Detached door panels are direct; interior door card is supporting context. |
| `body_mount_points_and_captive_nuts` | `direct_photo_evidence` | 10 | 87 | `body_mount_and_crossmember_detail|frame_and_mount_points` | Mount pedestal and frame-mount photos support thread/captive-nut condition checks before refit. |
| `body_rubbers` | `direct_photo_evidence` | 2 | 7 | `window_rubber_seals_and_frames` | Detached window assemblies with rubber surrounds are directly documented. |
| `brake_hydraulic_refresh_and_bias_decision` | `direct_photo_evidence` | 87 | 17 | `frame_floor_underside_and_lines` | Hard-line routing photos are direct evidence for hose/line refresh planning, with axle-end hardware views supporting brake-bias and wear decisions. |
| `brake_system_evidence_pack` | `direct_photo_evidence` | 113 | 2 | `frame_and_mount_points|frame_floor_underside_and_lines|rear_axle_and_leaf_springs|steering_and_suspension_linkages` | Brake evidence pack combines direct front/rear axle hardware views with underbody hard-line photos and supporting underside context. |
| `chassis_frame_and_crossmembers` | `direct_photo_evidence` | 97 | 17 | `frame_and_mount_points|frame_floor_underside_and_lines|rear_frame_crossmember_and_mounts` | Body-off underside shots provide direct evidence for rails/crossmembers and supporting suspension context. |
| `chassis_hard_lines_and_brackets` | `direct_photo_evidence` | 87 | 17 | `frame_floor_underside_and_lines` | Underbody routing photos give direct visibility to line paths/brackets and nearby support hardware. |
| `floor_pan` | `direct_photo_evidence` | 38 | 89 | `floor_pan_and_firewall|floor_pan_rust_zones|floor_seam_and_body_mount_rust` | Floor pan rust/condition is directly evidenced with dedicated close-ups. |
| `front_brake_disc_baseline` | `direct_photo_evidence` | 7 | 11 | `steering_and_suspension_linkages` | Steering-linkage underside photos are the closest grouped direct evidence, with frame/mount shots providing supporting context for the current front disc inference. |
| `front_windows` | `direct_photo_evidence` | 2 | 18 | `hood_and_front_windshield_overview` | Front windshield is explicitly captured in dedicated front overview shots. |
| `front_wings` | `direct_photo_evidence` | 36 | 3 | `wing_removal_and_body_lift_prep` | Front wing removal state is directly documented in the body-lift prep photo set. |
| `hood` | `direct_photo_evidence` | 2 | 16 | `hood_and_front_windshield_overview` | Hood panel/latches are explicitly visible in front overview shots. |
| `interior` | `direct_photo_evidence` | 47 | 4 | `cabin_overview|dashboard_and_cabin_stripdown|dashboard_lower_structure|dashboard_shell_and_cabin|driver_footwell_firewall_and_wiring|floor_pan_and_firewall|rear_cargo_floor` | Interior strip-down and cabin state are well documented. |
| `issue_body_mount_captive_thread_repair` | `direct_photo_evidence` | 10 | 87 | `body_mount_and_crossmember_detail|frame_and_mount_points` | Body-mount pedestal and mount-point photos cover captive-nut and sleeve/thread repair planning. |
| `issue_brake_fuel_line_clip_corrosion` | `direct_photo_evidence` | 87 | 17 | `frame_floor_underside_and_lines` | Underbody line-routing photos are the primary evidence for clip/bracket corrosion and hard-line condition checks. |
| `issue_chassis_ground_points_refresh` | `direct_photo_evidence` | 87 | 8 | `frame_floor_underside_and_lines` | Frame and lower bay views provide context for grounding point cleanup and re-termination planning. |
| `issue_crossmember_end_thinning_check` | `direct_photo_evidence` | 2 | 96 | `body_mount_and_crossmember_detail|rear_frame_crossmember_and_mounts` | Crossmember and mount-detail photos are used to inspect end-wall thinning and edge corrosion. |
| `issue_front_spring_hanger_crack_check` | `direct_photo_evidence` | 12 | 9 | `rear_axle_and_leaf_springs|suspension_or_linkage_mount` | Spring and hanger views provide direct evidence for crack/deformation checks around hanger brackets. |
| `issue_steering_box_mount_crack_check` | `direct_photo_evidence` | 7 | 11 | `steering_and_suspension_linkages` | Steering linkage and nearby mount photos are the baseline evidence set for steering-box mount crack checks. |
| `old_accessory_wiring` | `direct_photo_evidence` | 17 | 4 | `driver_footwell_firewall_and_wiring|driver_footwell_firewall_pass_through|firewall_and_dash_wiring|pedal_box_wiring` | Accessory/electrical removal and rebuild work has strong direct photo coverage. |
| `paint_returned_panels_refinished` | `direct_photo_evidence` | 18 | 4 | `refinished_hinges_brackets_and_trim|refinished_seat_or_mount_bracket|wiper_arm_or_linkage_hardware` | Off-vehicle refinished hardware/panel photos provide direct evidence of returned painted parts. |
| `paint_sendout_panels_manifest` | `direct_photo_evidence` | 20 | 38 | `detached_body_panels_and_doors|detached_doors_and_panels|rear_hatch_inner_panel` | Detached panel/door batches provide direct send-out readiness evidence for painting. |
| `paint_workshop_progress_media` | `direct_photo_evidence` | 41 | 19 | `off_vehicle_workstation_reference_video|panel_detail_and_markings|wing_removal_and_body_lift_prep` | In-progress workshop videos and panel-handling shots track painting/bodywork activity between send-out and return. |
| `rear_brake_drum_baseline` | `direct_photo_evidence` | 10 | 87 | `rear_axle_and_leaf_springs` | Rear axle underside shots are the main evidence set for drum hardware and parking-brake linkage condition. |
| `rear_fuel_tank` | `direct_photo_evidence` | 4 | 87 | `fuel_filler_side_panel|rear_cargo_floor` | Fuel tank-out context and tank-area access are documented in filler-side and rear-floor images. |
| `roof_shell` | `direct_photo_evidence` | 5 | 0 | `roof_gutter_and_window_channel` | Roof channel/rain gutter photos are direct evidence of roof shell condition. |
| `tub_refit_rubber_hardware_shim_stack` | `direct_photo_evidence` | 2 | 96 | `body_mount_and_crossmember_detail|floor_seam_and_body_mount_rust` | Current original-rubber evidence is limited to mount-detail and tub-side body-mount rust photos; these are enough for style/context but not for final sample dimensions. |
| `window_mechanisms` | `direct_photo_evidence` | 1 | 1 | `rear_hatch_window_latch_mechanisms` | Rear hatch window latch hardware is directly documented; wiper/linkage remains supporting evidence. |
