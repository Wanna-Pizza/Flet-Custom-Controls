import asyncio
import flet as ft

BUTTON_HEIGHT = 40
DEFAULT_BORDER_DARKMODE = ft.border.all(width=1, color='white,0.1')
DEFAULT_BORDER_LIGHTMODE = ft.border.all(width=0.5, color=ft.Colors.GREY_500)
DEFAULT_TEXTCOLOR_DARKMODE = ft.Colors.WHITE60
DEFAULT_TEXTCOLOR_LIGHTMODE = ft.Colors.BLACK87
DEFAULT_TEXTSTYLE_DARKMODE = ft.TextStyle(size=15, color= DEFAULT_TEXTCOLOR_DARKMODE)
DEFAULT_TEXTSTYLE_LIGHTMODE = ft.TextStyle(size=15, color= DEFAULT_TEXTCOLOR_LIGHTMODE)
DEFAULT_BG = "white,0.01"
DEFAULT_RADIUS = 10
DEFAULT_BLUR = 10
DEFAULT_ANIMATION_OPACITY = 300
DEFAULT_ANIMATION_SPEED = 300


class OverlayMenu(ft.Container):
    """
    Custom overlay menu for option selection.
    """

    def __init__(
            self,
            left: float = 0,
            top: float = 0,
            width: float = 200,
            on_select: callable = None,
            options=None,
            max_visible: int = 3,
    ):
        super().__init__()
        self._left = left
        self._top = top
        self._width = width
        self.options = options or []
        self.max_visible = max_visible
        self.on_select = on_select
        self.height_button = BUTTON_HEIGHT
        self.on_click = self.remove_menu
        self.text_color = DEFAULT_TEXTCOLOR_DARKMODE
        self.border = DEFAULT_BORDER_DARKMODE
        self.menu:ft.Container = self._create_menu()
        self.animate_opacity = DEFAULT_ANIMATION_OPACITY
        self.animate = DEFAULT_ANIMATION_SPEED

    def _build_button(self, text):

        def on_hover(e):
            color = 'white,0.05'
            if self.page:
                if self.page.theme_mode == ft.ThemeMode.LIGHT:
                    color = 'grey,0.15'
                else:
                    color = 'white,0.05'
            e.control.bgcolor = color if e.control.bgcolor != color else 'white,0.00'
            e.control.update()

        return ft.Container(
            content=ft.Text(text, size=16, color=self.text_color),
            on_click=lambda e: (self.on_select(text), self.remove_menu(e)),
            height=self.height_button - 8,
            on_hover=on_hover,
            padding=ft.padding.only(left=5,right=5),
            bgcolor= 'white,0.00',
            alignment=ft.alignment.center
        )

    def _build_menu_content(self):
        return ft.Column(
            [self._build_button(option) for option in self.options],
            scroll= ft.ScrollMode.AUTO if self.max_visible < self.options.__len__() else None,
            spacing=0,
        )

    def _create_menu(self):
        self.menu = ft.Container(
            height=0,
            width=self._width,
            left=self._left,
            top=self._top,
            border_radius=DEFAULT_RADIUS,
            blur=10,
            bgcolor=DEFAULT_BG,
            opacity=0,
            animate_opacity=ft.Animation(duration=self.animate_opacity, curve=ft.AnimationCurve.LINEAR_TO_EASE_OUT),
            animate=ft.Animation(duration=self.animate, curve=ft.AnimationCurve.LINEAR_TO_EASE_OUT),
            border=DEFAULT_BORDER_DARKMODE,
            content=self._build_menu_content()
        )
        return self.menu

    async def async_remove_menu(self, e):
        self.menu.height = 0
        self.menu.opacity = 0
        self.menu.update()
        await asyncio.sleep(0.01)
        self.page.overlay.remove(self)
        self.page.update()

    def remove_menu(self, e):
        self.page.run_task(self.async_remove_menu, e)

    async def on_mount(self):
        self.page.update()
        self._create_menu()
        self.page.overlay.append(self.menu)
        self.page.update()
        await asyncio.sleep(0.02)
        count = len(self.options)
        self.menu.height = ((self.height_button - 8) * min(count, self.max_visible)) + 2
        self.menu.opacity = 1
        self.menu.update()

    def before_update(self):
        super().before_update()
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.text_color = DEFAULT_TEXTCOLOR_LIGHTMODE
            self.menu.border = DEFAULT_BORDER_LIGHTMODE
        else:
            self.text_color = DEFAULT_TEXTCOLOR_DARKMODE
            self.menu.border = DEFAULT_BORDER_DARKMODE


    def did_mount(self):
        self.page.run_task(self.on_mount)
        return super().did_mount()


class DropDown(ft.Container):
    """
    Custom DropDown Menu.
    """

    def __init__(
            self,
            height: float = BUTTON_HEIGHT,
            width: float = 70,
            text_style: ft.TextStyle = DEFAULT_TEXTSTYLE_DARKMODE,
            default_value: str = "None",
            options=None,
            on_select: callable = None,
            max_visible: int = 3,
    ):
        super().__init__()
        self.on_select = on_select
        self.menu_text_style = text_style
        self.max_visible = max_visible
        self.options = options or []
        self.default_value = default_value
        self.height = height
        self.width = width
        self.text_display = ft.Text(value=self.default_value, style=self.menu_text_style)
        self.showing_container = ft.Container(
            self.text_display,
            blur= DEFAULT_BLUR,
            on_hover=self._on_hover,
            alignment=ft.alignment.center,
            border_radius=DEFAULT_RADIUS
        )
        self.content = self._build_content()

    def _on_hover(self, e):
        color = 'white,0.03'
        if self.page:
            if self.page.theme_mode == ft.ThemeMode.LIGHT:
                color = 'grey,0.1'
            else:
                color = 'white,0.03'
        e.control.bgcolor = color if e.control.bgcolor != color else DEFAULT_BG
        e.control.update()

    def get_value(self):
        return self.text_display.value

    def before_update(self):
        super().before_update()
        if self.page:
            if self.page.theme_mode == ft.ThemeMode.LIGHT:
                self.showing_container.border = DEFAULT_BORDER_LIGHTMODE
                self.text_display.style = DEFAULT_TEXTSTYLE_LIGHTMODE
            else:
                self.showing_container.border = DEFAULT_BORDER_DARKMODE
                self.text_display.style = DEFAULT_TEXTSTYLE_DARKMODE

    def _on_select(self, value):
        if self.on_select:
            self.on_select(value)
        self.text_display.value = value
        self.text_display.update()

    def on_tap_up(self, e: ft.TapEvent):
        top_left_x = e.global_x - e.local_x
        top_left_y = e.global_y - e.local_y + self.height + 5
        self.page.overlay.append(
            OverlayMenu(
                left=top_left_x,
                top=top_left_y,
                width=self.width,
                on_select=self._on_select,
                options=self.options,
                max_visible=self.max_visible,
            )
        )
        self.page.update()

    def _build_content(self):
        if self.page:
            if self.page.theme_mode == ft.ThemeMode.LIGHT:
                self.showing_container.border = DEFAULT_BORDER_LIGHTMODE
                self.text_display.style = DEFAULT_TEXTSTYLE_LIGHTMODE
            else:
                self.showing_container.border = DEFAULT_BORDER_DARKMODE
                self.text_display.style = DEFAULT_TEXTSTYLE_DARKMODE
        return ft.GestureDetector(
            content=self.showing_container,
            on_tap_up=self.on_tap_up,
            mouse_cursor=ft.MouseCursor.CLICK
        )
