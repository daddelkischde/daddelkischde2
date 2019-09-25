#!/bin/bash

backtitle="daddelkischde 2"
scriptdir="/home/pi/daddelkischde2/"

function show_msg()
{
	local msg="$1"
	
	dialog --backtitle "$backtitle" --msgbox "$msg" 10 40
}

function yes_no_box()
{
	local msg="$1"
	
	if dialog --backtitle "$backtitle" --yesno "$msg" 10 40 >/dev/tty; then
		return 0
	else
		return 1
	fi
}

function edit_file()
{
	local file="$1"
	local cmd=(dialog --backtitle "$backtitle" --editbox "$file" 22 76)
	local choice=$("${cmd[@]}" 2>&1 >/dev/tty)
	
    [[ -n "$choice" ]] && echo "$choice" >"$file"
}

function version()
{
	echo "$@" | gawk -F. '{ printf("%03d%03d%03d\n", $1,$2,$3); }'
}

function joystick_gui()
{
	local default
	
	while true; do
		local status=$(python ${scriptdir}control.py get_joystick_enabled)
		
		local cmd=(dialog --backtitle "$backtitle" --title "Joystick" --cancel-label "Back" --default-item "$default" --menu "Status: $status" 16 40 16)
		local options=(
			E "Enable"
			D "Disable"
			C "Calibrate"
		)
		
		local choice=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)
		
		if [[ -n "$choice" ]]; then
			case "$choice" in
				E)
					python ${scriptdir}control.py set_joystick_enabled
					;;
				D)
					python ${scriptdir}control.py set_joystick_disabled
					;;
				C)
					clear
					python ${scriptdir}calibrate_joystick.py
					;;
			esac
		else
			break
		fi
	done
}

function battery_monitor_gui()
{
	local default
	
	while true; do
		local status=$(systemctl is-active dk2_batmon.service)
		
		local cmd=(dialog --backtitle "$backtitle" --title "Battery monitor" --cancel-label "Back" --default-item "$default" --menu "Status: $status" 16 40 16)
		local options=(
			E "Enable"
			D "Disable"
			C "Edit configuration file"
		)
		
		local choice=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)
		
		if [[ -n "$choice" ]]; then
			default="$choice"
			
			case "$choice" in
				E)
					sudo systemctl enable dk2_batmon.service
					sudo systemctl start dk2_batmon.service
					;;
				D)
					sudo systemctl stop dk2_batmon.service
					sudo systemctl disable dk2_batmon.service
					;;
				C)
					edit_file "${scriptdir}batmon_config.py"
					;;
			esac
		else
			break
		fi
	done
}

function fan_control_gui()
{
	local default
	
	while true; do
		local status=$(systemctl is-active dk2_fan_control.service)
		local fan_state=$(python ${scriptdir}control.py get_fan)
		local temp=$(vcgencmd measure_temp)
		
		local cmd=(dialog --backtitle "$backtitle" --title "Fan control" --cancel-label "Back" --default-item "$default" --menu "Status: $status\nFan: $fan_state\nCPU $temp" 16 40 16)
		local options=(
			E "Enable automatic fan control"
			D "Disable automatic fan control"
			O "Turn fan on"
			F "Turn fan off"
			C "Edit configuration file"
		)
		
		local choice=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)
		
		if [[ -n "$choice" ]]; then
			default="$choice"
			
			case "$choice" in
				E)
					sudo systemctl enable dk2_fan_control.service
					sudo systemctl start dk2_fan_control.service
					;;
				D)
					sudo systemctl stop dk2_fan_control.service
					sudo systemctl disable dk2_fan_control.service
					;;
				O)
					python ${scriptdir}control.py fan_on
					;;
				F)
					python ${scriptdir}control.py fan_off
					;;
				C)
					edit_file "${scriptdir}fan_control_config.py"
					;;
			esac
		else
			break
		fi
	done
}

function safe_shutdown_gui()
{
	local default
	
	while true; do
		local status=$(systemctl is-active dk2_safe_shutdown.service)
		
		local cmd=(dialog --backtitle "$backtitle" --title "Safe shutdown" --cancel-label "Back" --default-item "$default" --menu "Status: $status" 16 40 16)
		local options=(
			E "Enable"
			D "Disable"
		)
		
		local choice=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)
		
		if [[ -n "$choice" ]]; then
			default="$choice"
			
			case "$choice" in
				E)
					sudo systemctl enable dk2_safe_shutdown.service
					sudo systemctl start dk2_safe_shutdown.service
					;;
				D)
					sudo systemctl stop dk2_safe_shutdown.service
					sudo systemctl disable dk2_safe_shutdown.service
					;;
			esac
		else
			break
		fi
	done
}

function boot_logo_gui()
{
	local default
	
	while true; do
		local display_time=$(python ${scriptdir}control.py get_logo_display)
	
		local cmd=(dialog --backtitle "$backtitle" --title "Boot logo" --cancel-label "Back" --default-item "$default" --menu "You can configure how long the boot logo is displayed (in milliseconds). Set to 0 to disable the boot logo.\n\nCurrent display time: $display_time ms" 16 40 16)
		local options=(
			C "Change display time"
		)
		
		local choice=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)
		
		if [[ -n "$choice" ]]; then
			default="$choice"
			
			case "$choice" in
				C)
					boot_logo_change_gui
					;;
			esac
		else
			break
		fi
	done
}

function boot_logo_change_gui()
{
	while true; do
		local display_time=$(python ${scriptdir}control.py get_logo_display)
		
		local cmd=(dialog --backtitle "$backtitle" --inputbox "Boot logo display time in milliseconds. Set to 0 to disable the boot logo." 10 40 $display_time)
		local choice=$("${cmd[@]}" 2>&1 >/dev/tty)
		
		if [[ -n "${choice//[0-9]/}" ]] || [[ "$choice" -lt 0 ]] || [[ "$choice" -gt 60000 ]]; then
			show_msg "Please enter a valid number between 0 and 60000!"
		elif [[ -n "$choice" ]]; then
			python ${scriptdir}control.py set_logo_display $choice
			break;
		else
			break;
		fi
	done
}

function button_combos_gui()
{
	local default
	
	while true; do
		local cmd=(dialog --backtitle "$backtitle" --title "Button combos" --cancel-label "Back" --default-item "$default" --menu "Button combinations for special functions." 22 60 16)
		local options=(
			I "Brightness increase"
			D "Brightness decrease"
			O "Fan on"
			F "Fan off"
		)
		
		local choice=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)
		
		if [[ -n "$choice" ]]; then
			default="$choice"
			
			case "$choice" in
				I)
					button_combo_edit_gui "brightness increase" "backlight_inc"
					;;
				D)
					button_combo_edit_gui "brightness decrease" "backlight_dec"
					;;
				O)
					button_combo_edit_gui "fan on" "fan_on"
					;;
				F)
					button_combo_edit_gui "fan off" "fan_off"
					;;
			esac
		else
			break
		fi
	done
}

function button_combo_edit_gui()
{
	local default
	local combo_name="$1"
	local combo_name_internal="$2"

	while true; do
		local buttons=$(python ${scriptdir}control.py get_button_combo $combo_name_internal)
		local options=()
	
		IFS=',' read -r -a options <<< "$buttons"
	
		local cmd=(dialog --backtitle "$backtitle" --title "Button combos" --cancel-label "Back" --default-item "$default" --checklist "Select the buttons you wish to use for $combo_name." 29 60 22)

		local choice=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)

		if [[ -n "$choice" ]]; then
			default="$choice"

			if [[ "${#choice}" -lt 3 ]]; then
				show_msg "At least two buttons are required!"
			else
				python ${scriptdir}control.py set_button_combo "$combo_name_internal" $choice
			fi
		else
			break
		fi
	done
}

function update_scripts_gui()
{
	local result=$(git -C ${scriptdir} pull)
	
	if [[ "$result" == "Already up-to-date." ]]; then
		show_msg "No update found."
	else
		show_msg "Scripts updated. Please reboot."
	fi
}

function update_firmware_gui()
{
	echo "Updating files..."
	
	git -C $scriptdir pull
	
	version_available=$(<${scriptdir}/firmware/version.txt)
	version_device=$(python ${scriptdir}control.py get_version)
	
	if [ "$(version "$version_available")" -gt "$(version "$version_device")" ]; then
		 if yes_no_box "An update to version $second_version is available!\nDo you want to update now?"; then
			${scriptdir}flash.sh
		 fi
	else
		show_msg "No update available."
	fi
}

function main_gui()
{
	local default
	
	while true; do
		local fw_version=$(python ${scriptdir}control.py get_version)
		local cmd=(dialog --backtitle "$backtitle" --title "daddelkischde 2 setup" --cancel-label "Exit" --default-item "$default" --menu "Firmware version: $fw_version" 18 60 16)
		local options=(
			J "Joystick"
			B "Battery monitor"
			F "Fan control"
			S "Safe shutdown"
			L "Boot logo"
			C "Button combos"
			R "Update scripts"
			U "Update firmware"
		)
		
		local choice=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)
		
		if [[ -n "$choice" ]]; then
			default="$choice"
			
			case "$choice" in
				J)
					joystick_gui
					;;
				B)
					battery_monitor_gui
					;;
				F)
					fan_control_gui
					;;
				S)
					safe_shutdown_gui
					;;
				L)
					boot_logo_gui
					;;
				C)
					button_combos_gui
					;;
				R)
					update_scripts_gui
					;;
				U)
					update_firmware_gui
					;;
			esac
		else
			break
		fi
	done
}

main_gui
