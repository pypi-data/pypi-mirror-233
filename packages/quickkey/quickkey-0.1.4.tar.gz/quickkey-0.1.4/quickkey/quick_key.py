from functools import partial
from pathlib import Path
import keyboard
import tkinter as tk
from multiprocessing import Process
import pystray
from PIL import Image
import os
from pkg_resources import resource_filename

def get_resource_path(res_name):
    try:
        # Try to get the resource path from an installed package
        return Path(resource_filename('quickkey', res_name))
    except(Exception):
        # If not installed, then directly access from the current directory structure
        base_path = os.path.abspath(os.path.dirname(__file__))
        return Path(os.path.join(base_path, res_name))

ico_path = get_resource_path('assets/quick_key.ico')




def worker():
    class LayerRemapper:
        def lp_on_key_down(self, e, initial_key, modified_key):
            if self.lp_is_key_down[initial_key]:
                return
            self.lp_is_key_down[initial_key] = True
            # Start a timer to check for long press
            def timer_function():
                if not self.lp_long_press_flag[initial_key] and self.lp_is_key_down[initial_key]:
                    if keyboard.is_modifier(modified_key):
                        keyboard.press(modified_key)
                    else:
                        keyboard.press_and_release(modified_key)
                    self.lp_long_press_flag[initial_key] = True

            keyboard.call_later(timer_function, delay=self.wait_time)

        def lp_on_key_up(self,e, initial_key, modified_key):
            self.lp_is_key_down[initial_key] = False

            if self.lp_long_press_flag[initial_key] and keyboard.is_modifier(modified_key):
                keyboard.release(modified_key)
            elif self.lp_long_press_flag[initial_key]:
                # Do nothing, as the key has already been pressed and released.
                pass
            else:
                keyboard.press_and_release(initial_key)

            # Reset the flag for next key press
            self.lp_long_press_flag[initial_key] = False

        def remap_key_long_press(self, initial_key, modified_key):
            
            self.lp_long_press_flag[initial_key] = False
            self.lp_is_key_down[initial_key] = False
            self.lp_initial_to_modified_key_map[initial_key] = modified_key

        def remap_key_layer_press(self, initial_key, modified_key):
            self.initial_to_modified_key_map[initial_key] = modified_key
        
        def activate_layer(self):
            for initial_key, modified_key in self.initial_to_modified_key_map.items():
                self.remap[initial_key] = keyboard.remap_key(initial_key, modified_key)

            for initial_key, modified_key in self.lp_initial_to_modified_key_map.items():
                keyboard.on_press_key(initial_key, partial(self.lp_on_key_down, initial_key = initial_key, modified_key=modified_key), suppress=True)
                keyboard.on_release_key(initial_key, partial(self.lp_on_key_up, initial_key = initial_key, modified_key=modified_key), suppress=True)
        def deactivate_layer(self):
            for mp in self.remap.values():
                keyboard.unremap_key(mp)
            self.remap = {}
            for mp in self.lp_remap.values():
                keyboard.unhook(mp)
            self.lp_remap = {}
        
        def __init__(self, activator, wait_time=.1):
            self.long_press_flag = False
            self.is_key_down = False
            self.wait_time = wait_time
            self.initial_to_modified_key_map = {}
            self.remap = {}
            self.lp_remap = {}
            self.lp_long_press_flag = {}
            self.lp_is_key_down = {}
            self.lp_initial_to_modified_key_map = {}

            def on_key_down(e):
                if self.is_key_down:
                    return
                self.is_key_down = True
                # Start a timer to check for long press
                def timer_function():
                    if not self.long_press_flag and self.is_key_down:
                        self.activate_layer()
                        self.long_press_flag = True

                keyboard.call_later(timer_function, delay=wait_time)

            def on_key_up(e):
                self.is_key_down = False
                if not self.long_press_flag:
                    keyboard.press_and_release(activator)
                self.deactivate_layer()
                # Reset the flag for next key press
                self.long_press_flag = False

            # Listen for key events
            if activator == "":
                self.activate_layer()
            else:
                keyboard.on_press_key(activator, on_key_down, suppress=True)
                keyboard.on_release_key(activator, on_key_up, suppress=True)

    main = LayerRemapper("")

    ly = LayerRemapper("space", .1)

    combo = LayerRemapper(".", .1)

    ly.remap_key_layer_press('h', 'left')
    ly.remap_key_layer_press('j', 'down')
    ly.remap_key_layer_press('k', 'up')
    ly.remap_key_layer_press('l', 'right')
    ly.remap_key_layer_press('e', 'home')
    ly.remap_key_layer_press('i', 'end')
    ly.remap_key_layer_press('1', 'f1')
    ly.remap_key_layer_press('2', 'f2')
    ly.remap_key_layer_press('3', 'f3')
    ly.remap_key_layer_press('4', 'f4')
    ly.remap_key_layer_press('5', 'f5')
    ly.remap_key_layer_press('6', 'f6')
    ly.remap_key_layer_press('7', 'f7')
    ly.remap_key_layer_press('8', 'f8')
    ly.remap_key_layer_press('9', 'f9')
    ly.remap_key_layer_press('0', 'f10')
    ly.remap_key_layer_press('-', 'f11')
    ly.remap_key_layer_press('=', 'f12')
    ly.remap_key_layer_press('tab', 'esc')
    ly.remap_key_layer_press('w', 'ctrl+s')
    ly.remap_key_layer_press('r', 'ctrl+y')
    ly.remap_key_layer_press('u', 'ctrl+z')
    ly.remap_key_layer_press('o', 'page down')
    ly.remap_key_layer_press('p', 'page up')
    ly.remap_key_layer_press('d', 'delete')
    ly.remap_key_layer_press('f', 'backspace')
    ly.remap_key_layer_press(';', 'enter')

    ly.remap_key_layer_press('x', 'ctrl+x')
    ly.remap_key_layer_press('c', 'ctrl+c')
    ly.remap_key_layer_press('v', 'ctrl+v')
    ly.remap_key_layer_press('m', 'menu')


    main.remap_key_long_press('a', 'alt')
    main.remap_key_long_press('s', 'shift')
    main.remap_key_long_press('c', 'ctrl')

    combo.remap_key_layer_press('a', 'a+n+d')

    main.activate_layer()
    keyboard.wait()

class QuickKeyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config(bg='white')
        # Create a button and pack it
        self.start_stop_btn = tk.Button(self, text="Start", command=self.toggle_process, width=20, height=5, bg='#2a4773',fg='white', font=('Tahoma', 26, "bold"), activebackground='#1c293d', activeforeground='white',relief=tk.FLAT,borderwidth=0)
        self.start_stop_btn.pack(expand=True, fill=tk.BOTH)
        self.geometry('250x300')
        self.title('QuickKey')
        # Process related variables
        self.process = None
        if ico_path.exists(): self.iconbitmap(ico_path)
        self.credit_label_1 = tk.Label(self, text="QuickKey by Jason Wang", font=('Tahoma', 11, "bold"), fg='white', bg='#1f2f47')
        self.credit_label_1.pack(expand=True, fill=tk.BOTH)
        self.credit_label_2 = tk.Label(self, text="@chungchunwang on GitHub", font=('Tahoma', 11, "bold"), fg='white', bg='#1f2f47')
        self.credit_label_2.pack(expand=True, fill=tk.BOTH)
        self.toggle_process()

    def toggle_process(self):
        if self.process and self.process.is_alive():
            self.process.terminate()
            self.process = None
            self.start_stop_btn.config(text="Start")
        else:
            self.process = Process(target=worker)
            self.process.start()
            self.start_stop_btn.config(text="Stop")
def start():
    app = QuickKeyApp()
    def quit_app(icon, _):
        icon.stop()
        app.destroy()

    def show_from_menu(icon, _):
        icon.stop()
        app.after(0,app.deiconify())
    def hide_to_menu():
        app.withdraw()
        menu=(pystray.MenuItem('Show', show_from_menu), pystray.MenuItem('Quit', quit_app))
        kwargs = {
            "name": "QuickKey","title":"QuickKey", "menu": menu
        }
        if ico_path.exists():
            kwargs['icon'] = Image.open(ico_path)
        icon=pystray.Icon(**kwargs)
        icon.run()

    app.protocol('WM_DELETE_WINDOW', hide_to_menu)
    app.mainloop()

if __name__ == "__main__":
    start()