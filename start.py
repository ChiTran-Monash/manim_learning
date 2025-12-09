from manimlib import *
# from matplotlib.pyplot import grid

#These example were taken from 3b1b's manim repository
#hello Chi Co
#This was added on github to test pull hahaha
#This was added on github to test pull hehehe
# This comment was added in experimenting branch
# conflict 2 was added here

class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)
        square = Square()

        self.play(ShowCreation(square))
        self.wait()
        self.play(ReplacementTransform(square, circle))
        self.wait()

        self.play(circle.animate.stretch(4, 0)) #first index is scale, second index is direction( 0:xmaxis, 1:yaxis, 2:zaxis)
        self.wait()
        self.play(circle.animate.stretch(2, 1))
        self.play(Rotate(circle, 90 * DEGREES))
        # self.embed()
        text = Text("""
            Oh Chi, you are so beautiful
        """)
        self.play(Write(text))


class AnimatingMethods(Scene):
    def construct(self):

        # Set white background
        # self.camera.background_color = WHITE


        grid = Tex(r"\rho").get_grid(10, 10, height=4)
        # grid.set_color(BLACK)  # Make grid black so it's visible on white background
        self.add(grid)

        # You can animate the application of mobject methods with the
        # ".animate" syntax:
        self.play(grid.animate.shift(LEFT))

        # For this example, calling grid.shift(LEFT) would shift the
        # grid one unit to the left, but both of the previous calls to
        # "self.play" animate that motion.

        # The same applies for any method, including those setting colors.
        self.play(grid.animate.set_color(YELLOW))
        self.wait()
        self.play(grid.animate.set_submobject_colors_by_gradient(BLUE, GREEN))
        # # Horizontal gradient (left to right) - DEFAULT
        # self.play(grid.animate.set_submobject_colors_by_gradient(BLUE, GREEN, direction=RIGHT))
        self.wait()
        self.play(grid.animate.set_height(TAU - MED_SMALL_BUFF))
        self.wait()

        # # The method Mobject.apply_complex_function lets you apply arbitrary
        # # complex functions, treating the points defining the mobject as
        # # complex numbers.
        self.play(grid.animate.apply_complex_function(np.exp), run_time=5)
        self.wait()

        # # Even more generally, you could apply Mobject.apply_function,
        # # which takes in functions form R^3 to R^3
        self.play(
            grid.animate.apply_function(
                lambda p: [ # For a point p = (x, y, z) this is the index in the matrix up there
                    p[0] + 0.5 * math.sin(p[1]), # New X coordinate
                    p[1] + 0.5 * math.sin(p[0]), # New Y coordinate
                    p[2]                         # Z coordinate unchanged
                ]
            ),
            run_time=5,
        )
        self.wait()


class TextExample(Scene):
    def construct(self):
        # To run this scene properly, you should have "Consolas" font in your computer
        # for full usage, you can see https://github.com/3b1b/manim/pull/680
        text = Text("Here is a text", font="Consolas", font_size=90)
        difference = Text(
            """
            The most important difference between Text and TexText is that\n
            you can change the font more easily, but can't use the LaTeX grammar
            """,
            font="Arial", font_size=24,
            # t2c is a dict that you can choose color for different text
            t2c={"Text": BLUE, "TexText": BLUE, "LaTeX": ORANGE}
        )
        VGroup(text, difference).arrange(DOWN, buff=1)
        self.play(Write(text))
        # self.play(FadeIn(difference, UP))
        self.play(Write(difference, run_time=5))
        self.wait(3)

        fonts = Text(
            "And you can also set the font according to different words",
            font="Arial",
            t2f={"font": "Consolas", "words": "Consolas"},
            t2c={"font": BLUE, "words": GREEN}
        )
        fonts.set_width(FRAME_WIDTH - 1)
        slant = Text(
            "And the same as slant and weight",
            font="Consolas",
            t2s={"slant": ITALIC},
            t2w={"weight": BOLD},
            t2c={"slant": ORANGE, "weight": RED}
        )
        VGroup(fonts, slant).arrange(DOWN, buff=0.8)
        self.play(FadeOut(text), FadeOut(difference, shift=DOWN))
        self.play(Write(fonts))
        self.wait()
        self.play(Write(slant))
        self.wait()


class TexTransformExample(Scene):
    def construct(self):
        to_isolate = ["B", "C", "=", "(", ")"]
        lines = VGroup(
            # Passing in muliple arguments to Tex will result
            # in the same expression as if those arguments had
            # been joined together, except that the submobject
            # hierarchy of the resulting mobject ensure that the
            # Tex mobject has a subject corresponding to
            # each of these strings.  For example, the Tex mobject
            # below will have 5 subjects, corresponding to the
            # expressions [A^2, +, B^2, =, C^2]
            Tex("A^2", "+", "B^2", "=", "C^2"),
            # Likewise here
            Tex("A^2", "=", "C^2", "-", "B^2"),
            # Alternatively, you can pass in the keyword argument
            # "isolate" with a list of strings that should be out as
            # their own submobject.  So the line below is equivalent
            # to the commented out line below it.
            Tex("A^2 = (C + B)(C - B)", isolate=["A^2", *to_isolate]),
            # OldTex("A^2", "=", "(", "C", "+", "B", ")", "(", "C", "-", "B", ")"),
            Tex("A = \\sqrt{(C + B)(C - B)}", isolate=["A", *to_isolate])
        )
        lines.arrange(DOWN, buff=LARGE_BUFF)
        for line in lines:
            line.set_color_by_tex_to_color_map({
                "A": BLUE,
                "B": TEAL,
                "C": GREEN,
            })

        play_kw = {"run_time": 2}
        self.add(lines[0])
        # The animation TransformMatchingTex will line up parts
        # of the source and target which have matching tex strings.
        # Here, giving it a little path_arc makes each part sort of
        # rotate into their final positions, which feels appropriate
        # for the idea of rearranging an equation
        self.play(
            TransformMatchingTex(
                lines[0].copy(), lines[1],
                path_arc=90 * DEGREES,
            ),
            **play_kw
        )
        self.wait()

        # Now, we could try this again on the next line...
        self.play(
            TransformMatchingTex(lines[1].copy(), lines[2]),
            **play_kw
        )
        self.wait()
        # ...and this looks nice enough, but since there's no tex
        # in lines[2] which matches "C^2" or "B^2", those terms fade
        # out to nothing while the C and B terms fade in from nothing.
        # If, however, we want the C^2 to go to C, and B^2 to go to B,
        # we can specify that with a key map.
        self.play(FadeOut(lines[2]))
        self.play(
            TransformMatchingTex(
                lines[1].copy(), lines[2],
                key_map={
                    "C^2": "C",
                    "B^2": "B",
                }
            ),
            **play_kw
        )
        self.wait()

        self.play(
            TransformMatchingTex(
                lines[2].copy(), lines[3],
                key_map={
                    "A^2": "A",
                },
            ),
            **play_kw
        )

        self.wait()

        # # And to finish off, a simple TransformMatchingShapes would work
        # # just fine.  But perhaps we want that exponent on A^2 to transform into
        # # the square root symbol.  At the moment, lines[2] treats the expression
        # # A^2 as a unit, so we might create a new version of the same line which
        # # separates out just the A.  This way, when TransformMatchingTex lines up
        # # all matching parts, the only mismatch will be between the "^2" from
        # # new_line2 and the "\sqrt" from the final line.  By passing in,
        # # transform_mismatches=True, it will transform this "^2" part into
        # # the "\sqrt" part.
        #OOPS seems like transform_mismatches is not working properly right now for python 3.13
        # new_line2 = Tex("A^2 = (C + B)(C - B)", isolate=["A", *to_isolate])
        # new_line2.replace(lines[2])
        # new_line2.match_style(lines[2])

        # self.play(
        #     TransformMatchingTex(
        #         new_line2, lines[3],
        #         transform_mismatches=True,
        #     ),
        #     **play_kw
        # )
        # self.wait(3)
        # self.play(FadeOut(lines, RIGHT))

        # Alternatively, if you don't want to think about breaking up
        # the tex strings deliberately, you can TransformMatchingShapes,
        # which will try to line up all pieces of a source mobject with
        # those of a target, regardless of the submobject hierarchy in
        # each one, according to whether those pieces have the same
        # shape (as best it can).
        source = Text("the morse code", height=1)
        target = Text("here come dots", height=1)

        # source = Text("Tran Chi Co", height=1)
        # target = Text("Du Tuyet Nhi", height=1)

        self.play(Write(source))
        self.wait()
        kw = {"run_time": 3, "path_arc": PI / 2}
        self.play(TransformMatchingShapes(source, target, **kw))
        self.wait()


        # self.play(TransformMatchingShapes(target, source, **kw))
        # self.wait()


# square = Square()
# print(square.get_width())
class UpdatersExample(Scene):
    def construct(self):
        square = Square()
        square.set_fill(BLUE_E, 1)

        # On all all frames, the constructor Brace(square, UP) will
        # be called, and the mobject brace will set its data to match
        # that of the newly constructed object
        brace = always_redraw(Brace, square, UP)
        print('brace created')

        text, number = label = VGroup(
            Text("Width = "),
            DecimalNumber(
                0,
                show_ellipsis=True,
                num_decimal_places=2,
                include_sign=True,
            )
        )
        label.arrange(RIGHT)

        # This ensures that the method deicmal.next_to(square)
        # is called on every frame
        always(label.next_to, brace, UP)
        # You could also write the following equivalent line
        # label.add_updater(lambda m: m.next_to(brace, UP))

        # If the argument itself might change, you can use f_always,
        # for which the arguments following the initial Mobject method
        # should be functions returning arguments to that method.
        # The following line ensures that decimal.set_value(square.get_y())
        # is called every frame
        f_always(number.set_value, square.get_width)
        # You could also write the following equivalent line
        # number.add_updater(lambda m: m.set_value(square.get_width()))

        self.add(square, brace, label)

        # Notice that the brace and label track with the square
        self.play(
            square.animate.scale(2),
            rate_func=there_and_back,
            run_time=2,
        )
        self.wait()
        self.play(
            square.animate.set_width(5, stretch=True),
            run_time=3,
        )
        self.wait()
        self.play(
            square.animate.set_width(2),
            run_time=3
        )
        self.wait()

        # In general, you can alway call Mobject.add_updater, and pass in
        # a function that you want to be called on every frame.  The function
        # should take in either one argument, the mobject, or two arguments,
        # the mobject and the amount of time since the last frame.
        now = self.time
        w0 = square.get_width()
        square.add_updater(
            lambda m: m.set_width(w0 * math.cos(self.time - now))
        )
        self.wait(4 * PI)

class CoordinateSystemExample(Scene):
    def construct(self):
        axes = Axes(
            # x-axis ranges from -1 to 10, with a default step size of 1
            x_range=(-1, 10),
            # y-axis ranges from -2 to 2 with a step size of 0.5
            y_range=(-2, 2, 0.5),
            # The axes will be stretched so as to match the specified
            # height and width
            height=6,
            width=10,
            # Axes is made of two NumberLine mobjects.  You can specify
            # their configuration with axis_config
            axis_config={
                "stroke_color": GREY_A,
                "stroke_width": 2,
            },
            # Alternatively, you can specify configuration for just one
            # of them, like this.
            y_axis_config={
                "include_tip": False,
            }
        )
        # Keyword arguments of add_coordinate_labels can be used to
        # configure the DecimalNumber mobjects which it creates and
        # adds to the axes
        axes.add_coordinate_labels(
            font_size=20,
            num_decimal_places=1,
        )

        # Add axis titles
        x_title = Text("Time (seconds)", font_size=24)
        y_title = Text("Position (meters)", font_size=24)
        y_title.rotate(90 * DEGREES)  # Rotate for vertical axis
        # Add main title
        main_title = Text("Position vs Time", font_size=36, color=BLUE)

        # Use always() to make titles follow the axes
        always(x_title.next_to, axes.x_axis, DOWN, 0.5)
        always(y_title.next_to, axes.y_axis, LEFT, 0.5)
        always(main_title.next_to, axes, UP, 0.5)

        self.add(axes, x_title, y_title, main_title)

        # Axes descends from the CoordinateSystem class, meaning
        # you can call call axes.coords_to_point, abbreviated to
        # axes.c2p, to associate a set of coordinates with a point,
        # like so:
        dot = Dot()
        dot.set_color(RED)

        dot.move_to(axes.c2p(0, 0))
        self.play(FadeIn(dot, scale=0.5))
        self.play(dot.animate.move_to(axes.c2p(3, 2)))
        self.wait()
        self.play(dot.animate.move_to(axes.c2p(5, 0.5)))
        self.wait()

        # Similarly, you can call axes.point_to_coords, or axes.p2c
        # print(axes.p2c(dot.get_center()))

        # We can draw lines from the axes to better mark the coordinates
        # of a given point.
        # Here, the always_redraw command means that on each new frame
        # the lines will be redrawn
        h_line = always_redraw(lambda: axes.get_h_line(dot.get_left()))
        v_line = always_redraw(lambda: axes.get_v_line(dot.get_bottom()))

        self.play(
            ShowCreation(h_line),
            ShowCreation(v_line),
        )
        self.play(dot.animate.move_to(axes.c2p(3, -2)))
        self.wait()
        self.play(dot.animate.move_to(axes.c2p(1, 1)))
        self.wait()

        # If we tie the dot to a particular set of coordinates, notice
        # that as we move the axes around it respects the coordinate
        # system defined by them.
        f_always(dot.move_to, lambda: axes.c2p(1, 1))
        self.play(
            axes.animate.scale(0.75).to_corner(UL),
            main_title.animate.scale(0.75),
            x_title.animate.scale(0.75),
            y_title.animate.scale(0.75),
            run_time=2,
        )
        self.wait()

        # Clear updaters before fading out, so that the h_line, v_line,
        # and dot don't try to update while they're being faded out
        h_line.clear_updaters()
        v_line.clear_updaters()
        dot.clear_updaters()

        self.play(FadeOut(VGroup(axes, dot, h_line, v_line, x_title, y_title, main_title)))
        # self.play(FadeOut(VGroup(h_line, v_line)))

        # Other coordinate systems you can play around with include
        # ThreeDAxes, NumberPlane, and ComplexPlane.


class GraphExample(Scene):
    def construct(self):
        axes = Axes((-3, 10), (-5, 5), width=10, height=6)
        axes.add_coordinate_labels()

        self.play(Write(axes, lag_ratio=0.01, run_time=1))

        # Axes.get_graph will return the graph of a function
        sin_graph = axes.get_graph(
            lambda x: 2 * math.sin(x),
            color=BLUE,
        )
        # By default, it draws it so as to somewhat smoothly interpolate
        # between sampled points (x, f(x)).  If the graph is meant to have
        # a corner, though, you can set use_smoothing to False
        relu_graph = axes.get_graph(
            lambda x: max(x, 0),
            use_smoothing=False,
            color=YELLOW,
        )
        # For discontinuous functions, you can specify the point of
        # discontinuity so that it does not try to draw over the gap.
        step_graph = axes.get_graph(
            lambda x: 2.0 if x > 3 else 1.0,
            discontinuities=[3],
            color=GREEN,
        )

        # Axes.get_graph_label takes in either a string or a mobject.
        # If it's a string, it treats it as a LaTeX expression.  By default
        # it places the label next to the graph near the right side, and
        # has it match the color of the graph
        sin_label = axes.get_graph_label(sin_graph, "\\sin(x)")
        relu_label = axes.get_graph_label(relu_graph, Text("ReLU"))
        step_label = axes.get_graph_label(step_graph, Text("Step"), x=4)

        self.play(
            ShowCreation(sin_graph),
            FadeIn(sin_label, RIGHT),
        )
        self.wait(2)
        self.play(
            ReplacementTransform(sin_graph, relu_graph),
            FadeTransform(sin_label, relu_label),
        )
        self.wait()
        self.play(
            ReplacementTransform(relu_graph, step_graph),
            FadeTransform(relu_label, step_label),
        )
        self.wait()

        parabola = axes.get_graph(lambda x: 0.25 * x**2)
        parabola.set_stroke(BLUE)
        self.play(
            FadeOut(step_graph),
            FadeOut(step_label),
            ShowCreation(parabola)
        )
        self.wait()

        # You can use axes.input_to_graph_point, abbreviated
        # to axes.i2gp, to find a particular point on a graph
        dot = Dot()
        dot.set_color(RED)
        dot.move_to(axes.i2gp(2, parabola))
        self.play(FadeIn(dot, scale=0.5))

        # A value tracker lets us animate a parameter, usually
        # with the intent of having other mobjects update based
        # on the parameter
        x_tracker = ValueTracker(2)
        f_always(
            dot.move_to,
            lambda: axes.i2gp(x_tracker.get_value(), parabola)
        )

        self.play(x_tracker.animate.set_value(4), run_time=3)
        self.play(x_tracker.animate.set_value(-2), run_time=3)
        self.wait()

class SurfaceExample(Scene):
    CONFIG = {
        "camera_class": ThreeDCamera,
    }

    def construct(self):
        surface_text = Text("3D Surfaces Demo")
        surface_text.fix_in_frame()
        surface_text.to_edge(UP)
        self.add(surface_text)
        self.wait(0.1)

        # Create 3D objects without textures to avoid network issues
        torus1 = Torus(r1=1, r2=1)
        torus2 = Torus(r1=3, r2=1)
        sphere = Sphere(radius=3, resolution=torus1.resolution)

        # Set colors instead of textures
        surfaces = [
            sphere.set_color(BLUE),
            torus1.set_color(GREEN), 
            torus2.set_color(RED)
        ]

        # Add wireframe meshes
        for i, mob in enumerate(surfaces):
            mob.shift(IN)
            mob.mesh = SurfaceMesh(mob)
            # Different mesh colors for variety
            mesh_colors = [WHITE, YELLOW, PURPLE]
            mob.mesh.set_stroke(mesh_colors[i], 1, opacity=0.3)

        # Set camera perspective
        frame = self.camera.frame
        frame.set_euler_angles(
            theta=-30 * DEGREES,
            phi=70 * DEGREES,
        )

        surface = surfaces[0]

        # Animate first surface
        self.play(
            FadeIn(surface),
            ShowCreation(surface.mesh, lag_ratio=0.01, run_time=3),
        )
        
        # Add mesh to surface groups
        for mob in surfaces:
            mob.add(mob.mesh)
        
        surface.save_state()
        self.play(Rotate(surface, PI / 2), run_time=2)
        
        # Prepare other surfaces for transformation
        for mob in surfaces[1:]:
            mob.rotate(PI / 2)

        # Transform to torus1
        self.play(
            Transform(surface, surfaces[1]),
            run_time=3
        )

        # Transform to torus2
        self.play(
            Transform(surface, surfaces[2]),
            # Move camera frame during the transition
            frame.animate.increment_phi(-10 * DEGREES),
            frame.animate.increment_theta(-20 * DEGREES),
            run_time=3
        )
        
        # Add ambient rotation
        frame.add_updater(lambda m, dt: m.increment_theta(-0.1 * dt))
        self.wait(3)

        # Clean up rotation updater
        frame.clear_updaters()

        # Light demonstration (without texture dependency)
        light_text = Text("Camera and lighting effects", font_size=24)
        light_text.move_to(surface_text)
        light_text.fix_in_frame()

        self.play(FadeTransform(surface_text, light_text))
        
        # Demonstrate camera movement
        self.play(
            frame.animate.increment_phi(45 * DEGREES),
            frame.animate.increment_theta(90 * DEGREES),
            run_time=4
        )
        
        self.play(
            frame.animate.increment_phi(-45 * DEGREES),
            frame.animate.increment_theta(-90 * DEGREES),
            run_time=4
        )

        interaction_text = Text("3D Scene Complete!", font_size=28, color=YELLOW)
        interaction_text.move_to(light_text)
        interaction_text.fix_in_frame()

        self.play(FadeTransform(light_text, interaction_text))
        self.wait(2)

class OpeningManimExample(Scene):
    def construct(self):
        intro_words = Text("""
            The original motivation for manim was to
            better illustrate mathematical functions
            as transformations.
        """)
        intro_words.to_edge(UP)

        self.play(Write(intro_words))
        self.wait(2)

        # Linear transform
        # grid = NumberPlane((-10, 10), (-5, 5))
        #can do this if the grid density is too high
        grid = NumberPlane(
            x_range=(-10, 10, 2),    # Step of 2 instead of default 1
            y_range=(-5, 5, 2),      # Step of 2 instead of default 0.5
        )
        matrix = [[1, 1], [0, 1]]
        # Create matrix without the problematic parameter
        matrix_mob = IntegerMatrix(matrix)
        # Add background rectangle manually if needed
        matrix_mob.add_background_rectangle(color=BLACK, opacity=0.8)
        linear_transform_words = VGroup(
            Text("This is what the matrix"),
            matrix_mob,
            Text("looks like")
        )
        linear_transform_words.arrange(RIGHT)
        linear_transform_words.to_edge(UP)
        linear_transform_words.set_stroke(BLACK, 3, behind=True)

        self.play(
            ShowCreation(grid),
            FadeTransform(intro_words, linear_transform_words)
        )
        self.wait()
        self.play(grid.animate.apply_matrix(matrix), run_time=3)
        self.wait()

        # # Complex map
        # c_grid = ComplexPlane()
        c_grid = ComplexPlane(
            x_range=(-10,10, 2),    # Step of 2 instead of default 0.5
            y_range=(-5, 5, 2),    # Step of 2 instead of default 0.5
        )

        moving_c_grid = c_grid.copy()
        moving_c_grid.prepare_for_nonlinear_transform()
        c_grid.set_stroke(BLUE_E, 1)
        c_grid.add_coordinate_labels(font_size=24)
        complex_map_words = TexText("""
            Or thinking of the plane as $\\mathds{C}$,\\\\
            this is the map $z \\rightarrow z^2$
        """)
        complex_map_words.to_corner(UR)
        complex_map_words.set_stroke(BLACK, 3, behind=True)

        self.play(
            FadeOut(grid),
            Write(c_grid, run_time=3),
            FadeIn(moving_c_grid),
            FadeTransform(linear_transform_words, complex_map_words),
        )
        self.wait()
        self.play(
            moving_c_grid.animate.apply_complex_function(lambda z: z**2),
            run_time=6,
        )
        self.wait(2)
