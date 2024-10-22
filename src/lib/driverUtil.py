def close_handles(driver):
    handles = driver.window_handles

    main_handle = driver.current_window_handle
    for x in range(len(handles)):
    	if handles[x] != main_handle:
    		driver.switch_to.window(handles[x])
    		driver.close()

    driver.switch_to.window(main_handle)