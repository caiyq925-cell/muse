"""
智能客服满意度问题 —— ManimCE 讲解动画（3Blue1Brown 风格）
主线讲法：单位"1"连乘 + 0~1 标尺上的满意度条
关键一跳：第 3 幕 ——「又提高 1/4」的单位"1"是当下的 18/25，不是最初的 3/5
渲染：python -m manim -qm smart_service_satisfaction.py SmartServiceSatisfaction
"""
from manim import *
from fractions import Fraction

# ---------- 配色（同一颜色全片只表达同一意思） ----------
BG     = "#0B1026"   # 深色背景
C_COND = "#00D9FF"   # 青：条件
C_KEY  = "#FFC24B"   # 黄：关键一跳与最终答案
C_CHG  = "#FF6B9D"   # 粉：变化 / 新增部分
C_OK   = "#2ED3A6"   # 绿：验算通过
C_TXT  = "#FFFFFF"   # 白：正文
C_SEC  = "#A9B4D8"   # 灰蓝：次要说明
CJK    = "Noto Sans SC"

config.background_color = BG

# ---------- 最终答案与全部上屏数字的唯一来源 ----------
F_ORIG = Fraction(3, 5)      # 原满意度
R_AI   = Fraction(6, 5)      # 智能客服单独服务：是原来的 6/5
R_UP   = Fraction(1, 4)      # 双重服务：又提高 1/4
R_DUAL = 1 + R_UP            # = 5/4
F_MID  = F_ORIG * R_AI       # 中间结果 18/25
F_ANS  = F_MID * R_DUAL      # 最终答案 9/10

assert F_MID == Fraction(18, 25)
assert F_ANS == Fraction(9, 10)
# 代回验算（逆向除回）
assert F_ANS / R_DUAL == F_MID
assert F_MID / R_AI == F_ORIG
# 交叉验算（化小数）
assert abs(float(F_ORIG) * float(R_AI) * float(R_DUAL) - float(F_ANS)) < 1e-12

# 求解幕的展开中间式 90/100（由答案派生，不手敲）
NUM10 = F_ANS.numerator * 10   # 90
DEN10 = F_ANS.denominator * 10  # 100

AX_L, AX_R, AY = -6.4, 6.4, -1.3   # 0~1 标尺
AX_W = AX_R - AX_L
BAR_H = 0.58


def fr(x):
    """MathTex 用分数串"""
    return r"\frac{%d}{%d}" % (x.numerator, x.denominator)


def frt(x):
    """Text 行文用分数串"""
    return "%d/%d" % (x.numerator, x.denominator)


def fx(x):
    """小数串"""
    return "%g" % float(x)


def cell_bar(n_total, n_filled, cell_w, cell_h, gap, fill_color):
    """左端对齐的格子条：前 n_filled 格填色，空格用浅色描边保证可辨"""
    cells = VGroup()
    for i in range(n_total):
        filled = i < n_filled
        r = RoundedRectangle(
            width=cell_w, height=cell_h, corner_radius=0.08,
            stroke_width=2.5,
            stroke_color=fill_color if filled else C_SEC,
            fill_color=fill_color,
            fill_opacity=0.55 if filled else 0.08,
        )
        r.move_to([cell_w / 2 + i * (cell_w + gap), 0, 0])
        cells.add(r)
    return cells


def mkbox(tex_str, color, font_size=44):
    """幕 2 链条中的方框"""
    rect = RoundedRectangle(
        width=1.45, height=1.0, corner_radius=0.16,
        stroke_color=color, stroke_width=3,
        fill_color=C_TXT, fill_opacity=0.05,
    )
    m = MathTex(tex_str, font_size=font_size, color=color)
    return VGroup(rect, m)


def make_axis():
    """0~1 标尺（幕 3 的参照物，全程不动）"""
    ax = Line([AX_L, AY, 0], [AX_R, AY, 0], stroke_width=3, color=C_TXT)
    ticks = VGroup(*[
        Line([AX_L + AX_W * (k + 1) / 5, AY - 0.09, 0],
             [AX_L + AX_W * (k + 1) / 5, AY + 0.09, 0],
             stroke_width=2.5, color=C_TXT)
        for k in range(5)
    ])
    lab0 = Text("0", font=CJK, font_size=20, color=C_SEC).next_to(ax.get_start(), DOWN, buff=0.18)
    lab1 = Text("1", font=CJK, font_size=20, color=C_SEC).next_to(ax.get_end(), DOWN, buff=0.18)
    return VGroup(ax, ticks, lab0, lab1)


def ghost_line(x):
    """旧位置的粉色虚线残影"""
    return DashedLine([x, AY, 0], [x, AY + 0.85, 0],
                      dash_length=0.14, stroke_width=2.5, color=C_CHG)


def inc_rect(f1, f2):
    """条上新增的粉色段"""
    return RoundedRectangle(
        width=AX_W * (f2 - f1), height=BAR_H, corner_radius=0.06,
        stroke_color=C_CHG, stroke_width=2,
        fill_color=C_CHG, fill_opacity=0.6,
    ).move_to([AX_L + AX_W * (f1 + f2) / 2, AY + BAR_H / 2, 0])


def bar_at(f):
    """以 0~1 标尺上比例 f 画满意度条（左端贴 0）"""
    w = AX_W * f
    return RoundedRectangle(
        width=w, height=BAR_H, corner_radius=0.06,
        stroke_color=C_COND, stroke_width=2.5,
        fill_color=C_COND, fill_opacity=0.55,
    ).move_to([AX_L + w / 2, AY + BAR_H / 2, 0])


class SmartServiceSatisfaction(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ============ 全片固定：顶部主标题（仅答案卡一幕淡出） ============
        title = Text("智能客服满意度问题", font=CJK, font_size=30, color=C_TXT)
        title.to_edge(UP, buff=0.32)
        self.add(title)

        def step(txt):
            return Text(txt, font=CJK, font_size=22, color=C_SEC).to_corner(UL, buff=0.5).shift(DOWN * 0.5)

        # ==================== 幕 1 · 题目登场 ====================
        s1 = step("第 1 步 · 看题目")
        self.play(FadeIn(s1, shift=DOWN * 0.2), run_time=0.5)

        bar5 = cell_bar(5, F_ORIG.numerator, 1.9, 0.62, 0.06, C_COND)
        bar5.move_to([0, 1.55, 0])
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in bar5], lag_ratio=0.15),
                  run_time=1.0)
        lab5 = VGroup(
            MathTex(fr(F_ORIG), font_size=40, color=C_COND),
            Text(" 原来的满意度", font=CJK, font_size=22, color=C_SEC),
        ).arrange(RIGHT, buff=0.18).move_to([0, 0.72, 0])
        self.play(FadeIn(lab5), run_time=0.5)

        conds = VGroup(
            Text(f"① 客服人数少，满意度只有 {frt(F_ORIG)}", font=CJK, font_size=26, color=C_COND),
            Text(f"② 智能客服单独服务：满意度是原来的 {frt(R_AI)}", font=CJK, font_size=26, color=C_COND),
            Text(f"③ 双重服务：满意度又提高了 {frt(R_UP)}", font=CJK, font_size=26, color=C_COND),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36)
        conds.to_edge(LEFT, buff=0.78).shift(DOWN * 0.72)
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.4) for c in conds], lag_ratio=0.5),
                  run_time=1.6)
        q = Text("那么，现在的满意度是多少？", font=CJK, font_size=28,
                 color=C_TXT, weight=BOLD)
        q.to_edge(LEFT, buff=0.78).shift(DOWN * 2.42)
        self.play(FadeIn(q, shift=RIGHT * 0.4), run_time=0.6)
        self.wait(0.9)

        # ==================== 幕 2 · 翻译条件（只建模，不计算） ====================
        s2 = step("第 2 步 · 建模型")
        self.play(FadeOut(conds), FadeOut(q), FadeOut(s1), FadeIn(s2), run_time=0.5)
        self.play(bar5.animate.move_to([0, 2.05, 0]),
                  lab5.animate.move_to([0, 1.42, 0]), run_time=0.5)

        box1 = mkbox(fr(F_ORIG), C_COND)
        box2 = mkbox("?", C_SEC)
        box3 = mkbox("?", C_SEC)
        a1 = Arrow(ORIGIN, RIGHT * 1.15, buff=0, stroke_width=5, color=C_COND)
        a2 = Arrow(ORIGIN, RIGHT * 1.6, buff=0, stroke_width=5, color=C_COND)
        row = VGroup(box1, a1, box2, a2, box3).arrange(RIGHT, buff=0.42)
        row.move_to([0, -0.45, 0])
        t1 = MathTex(r"\times", fr(R_AI), font_size=34, color=C_COND)
        t1.next_to(a1, UP, buff=0.14)
        t2 = MathTex(r"\times\left(1+", fr(R_UP), r"\right)", font_size=34, color=C_COND)
        t2.next_to(a2, UP, buff=0.14)
        chain = VGroup(row, t1, t2)
        self.play(LaggedStart(
            FadeIn(box1, scale=0.7),
            FadeIn(a1, shift=RIGHT * 0.3), FadeIn(t1, scale=0.7),
            FadeIn(box2, scale=0.7),
            FadeIn(a2, shift=RIGHT * 0.3), FadeIn(t2, scale=0.7),
            FadeIn(box3, scale=0.7),
            lag_ratio=0.22), run_time=2.4)
        note = Text(
            f"「是原来的 {frt(R_AI)}」→ 乘 {frt(R_AI)}　　「又提高 {frt(R_UP)}」→ 乘（1+{frt(R_UP)}）",
            font=CJK, font_size=22, color=C_SEC,
        ).move_to([0, -2.35, 0])
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.6)
        self.wait(0.9)

        # ==================== 幕 3 · 关键一跳（⭐） ====================
        s3 = step("第 3 步 · 关键一跳")
        self.play(FadeOut(chain), FadeOut(note), FadeOut(bar5), FadeOut(lab5),
                  FadeOut(s2), FadeIn(s3), run_time=0.5)

        axis = make_axis()
        self.play(Create(axis), run_time=0.7)
        f0, f1_, f2_ = float(F_ORIG), float(F_MID), float(F_ANS)
        x0 = AX_L + AX_W * f0       # 3/5 的位置
        x1 = AX_L + AX_W * f1_      # 18/25 的位置
        x2 = AX_L + AX_W * f2_      # 9/10 的位置

        barA = bar_at(f0)
        self.play(GrowFromEdge(barA, LEFT), run_time=0.6)
        labA = MathTex(fr(F_ORIG), font_size=38, color=C_COND)
        labA.next_to(barA, UP, buff=0.16, aligned_edge=RIGHT).shift(RIGHT * 0.18)
        self.play(FadeIn(labA), run_time=0.4)

        # 第一次放大：×6/5
        g1 = ghost_line(x0)
        mul1 = Text(f"乘 {frt(R_AI)}", font=CJK, font_size=22, color=C_COND)
        mul1.move_to([(x0 + x1) / 2, -1.95, 0])
        barB = bar_at(f1_)
        labB = MathTex(fr(F_MID), font_size=38, color=C_COND)
        labB.next_to(barB, UP, buff=0.16, aligned_edge=RIGHT).shift(RIGHT * 0.18)
        inc1 = inc_rect(f0, f1_)
        self.play(FadeIn(g1), FadeIn(mul1, shift=UP * 0.15), run_time=0.5)
        self.play(ReplacementTransform(barA, barB),
                  ReplacementTransform(labA, labB),
                  FadeIn(inc1), run_time=1.1)
        self.wait(0.5)

        # ⭐ 关键一跳：单位"1"换成 18/25
        w18 = x1 - AX_L
        splits = VGroup(*[
            DashedLine([x1 - w18 * k / 4, AY, 0], [x1 - w18 * k / 4, AY + BAR_H, 0],
                       dash_length=0.11, stroke_width=2, color=C_TXT)
            for k in (1, 2, 3)
        ])
        self.play(barB.animate.set_stroke(color=C_KEY, width=4.5),
                  FadeOut(mul1), run_time=0.45)
        self.play(LaggedStart(*[Create(l) for l in splits], lag_ratio=0.25), run_time=0.8)
        block = RoundedRectangle(
            width=w18 / 4, height=BAR_H, corner_radius=0.06,
            stroke_color=C_CHG, stroke_width=2.5,
            fill_color=C_CHG, fill_opacity=0.9,
        ).move_to([x1 - w18 / 8, AY + BAR_H / 2, 0])
        blk_c = block.get_center()
        self.play(FadeIn(block, shift=UP * 0.3), run_time=0.45)
        self.play(block.animate.move_to(blk_c), run_time=0.35)
        labq = Text("这个 1/4", font=CJK, font_size=22, color=C_CHG)
        labq.move_to([x1 - w18 / 8 - 0.25, -1.9, 0])
        self.play(FadeIn(labq), run_time=0.4)
        punch = Text(f"单位「1」变了：这次的 {frt(R_UP)}，是 {frt(F_MID)} 的 {frt(R_UP)}",
                     font=CJK, font_size=26, color=C_KEY, weight=BOLD)
        punch.move_to([0, 1.78, 0])
        subn = Text("（参照物 0~1 标尺不动，动的只有满意度条）",
                    font=CJK, font_size=20, color=C_SEC)
        subn.move_to([0, 1.2, 0])
        self.play(FadeIn(punch, shift=UP * 0.2), FadeIn(subn), run_time=0.8)
        self.wait(0.6)

        # 第二次放大：×5/4
        g2 = ghost_line(x1)
        mul2 = Text(f"乘 {frt(R_DUAL)}", font=CJK, font_size=22, color=C_COND)
        mul2.move_to([(x1 + x2) / 2, -1.95, 0])
        barC = bar_at(f2_)
        labC = MathTex(fr(F_ANS), font_size=46, color=C_KEY)
        labC.next_to(barC, UP, buff=0.16, aligned_edge=RIGHT).shift(RIGHT * 0.18)
        inc2 = inc_rect(f1_, f2_)
        self.play(FadeOut(labq), FadeIn(g2), FadeIn(mul2, shift=UP * 0.15), run_time=0.5)
        self.play(ReplacementTransform(barB, barC),
                  ReplacementTransform(labB, labC),
                  FadeIn(inc2), run_time=1.1)
        self.play(Indicate(labC, color=C_KEY, scale_factor=1.25), run_time=0.6)
        self.wait(0.9)
        stage3 = VGroup(axis, barC, labC, g1, g2, mul2,
                        splits, block, punch, subn, inc1, inc2)

        # ==================== 幕 4 · 求解 ====================
        s4 = step("第 4 步 · 列式求解")
        self.play(FadeOut(stage3), FadeOut(s3), FadeIn(s4), run_time=0.6)
        eqs = VGroup(
            MathTex(fr(F_ORIG), r"\times", fr(R_AI), r"=", fr(F_MID), font_size=38),
            MathTex(fr(F_MID), r"\times\left(1+", fr(R_UP), r"\right)", font_size=38),
            MathTex(r"=", fr(F_MID), r"\times", fr(R_DUAL), font_size=38),
            MathTex(r"=", r"\frac{%d}{%d}" % (NUM10, DEN10), font_size=38),
            MathTex(r"=", fr(F_ANS), font_size=42),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        eqs.to_edge(LEFT, buff=0.85).shift(UP * 0.2)
        eqs[0][0].set_color(C_COND); eqs[0][2].set_color(C_COND); eqs[0][4].set_color(C_KEY)
        eqs[1][0].set_color(C_KEY); eqs[1][2].set_color(C_COND)
        eqs[2][1].set_color(C_KEY); eqs[2][3].set_color(C_COND)
        eqs[3][1].set_color(C_KEY)
        eqs[4][1].set_color(C_KEY)
        for e in eqs:
            self.play(FadeIn(e, shift=RIGHT * 0.35), run_time=0.55)
            self.wait(0.3)
        note2 = Text(
            f"另法：化小数 {fx(F_ORIG)} → ×{fx(R_AI)} 得 {fx(F_MID)} → ×{fx(R_DUAL)} 得 {fx(F_ANS)}",
            font=CJK, font_size=20, color=C_SEC,
        ).to_edge(LEFT, buff=0.85).shift(DOWN * 2.85)
        self.play(FadeIn(note2), run_time=0.5)
        self.wait(0.9)

        # ==================== 幕 5 · 验算 ====================
        s5 = step("第 5 步 · 代回验算")
        self.play(FadeOut(eqs), FadeOut(note2), FadeOut(s4), FadeIn(s5), run_time=0.5)
        bar10 = cell_bar(10, F_ANS.numerator, 1.05, 0.6, 0.05, C_OK)
        bar10.move_to([0, 1.85, 0])
        nums = VGroup(*[
            Text(str(i + 1), font=CJK, font_size=15, color=C_SEC)
            .move_to([c.get_x(), 1.42, 0])
            for i, c in enumerate(bar10)
        ])
        lab10 = MathTex(fr(F_ANS), font_size=40, color=C_OK).move_to([6.15, 1.85, 0])
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in bar10], lag_ratio=0.1),
                  run_time=1.1)
        self.play(FadeIn(nums), FadeIn(lab10), run_time=0.5)

        r1 = VGroup(
            MathTex(fr(F_ANS), r"\div", fr(R_DUAL), r"=", fr(F_MID), font_size=34, color=C_TXT),
            Text("　回到双重服务前", font=CJK, font_size=20, color=C_SEC),
            MathTex(r"\checkmark", font_size=34, color=C_OK),
        ).arrange(RIGHT, buff=0.25).to_edge(LEFT, buff=0.85).shift(UP * 0.3)
        r2 = VGroup(
            MathTex(fr(F_MID), r"\div", fr(R_AI), r"=", fr(F_ORIG), font_size=34, color=C_TXT),
            Text("　回到最初的满意度", font=CJK, font_size=20, color=C_SEC),
            MathTex(r"\checkmark", font_size=34, color=C_OK),
        ).arrange(RIGHT, buff=0.25).to_edge(LEFT, buff=0.85).shift(DOWN * 0.62)
        r3 = VGroup(
            Text(f"{frt(F_ANS)} 没超过 1（在 0~1 标尺内），合理",
                 font=CJK, font_size=24, color=C_TXT),
            MathTex(r"\checkmark", font_size=34, color=C_OK),
        ).arrange(RIGHT, buff=0.3).to_edge(LEFT, buff=0.85).shift(DOWN * 1.55)
        for r in (r1, r2, r3):
            self.play(FadeIn(r, shift=UP * 0.15), run_time=0.55)
            self.play(Indicate(r[-1], color=C_OK, scale_factor=1.4), run_time=0.4)
        self.wait(1.0)

        # ==================== 幕 6 · 答案卡 ====================
        self.play(*[FadeOut(m) for m in (title, s5, bar10, nums, lab10, r1, r2, r3)],
                  run_time=0.7)
        card = RoundedRectangle(
            width=10.6, height=2.7, corner_radius=0.35,
            stroke_color=C_KEY, stroke_width=4,
            fill_color=C_TXT, fill_opacity=0.04,
        ).move_to([0, 0.2, 0])
        a_lab = Text("答案", font=CJK, font_size=24, color=C_SEC).move_to([0, 0.95, 0])
        a_val = VGroup(
            Text("现在的满意度是 ", font=CJK, font_size=40, color=C_KEY, weight=BOLD),
            MathTex(fr(F_ANS), font_size=56, color=C_KEY),
        ).arrange(RIGHT, buff=0.22).move_to([0, -0.05, 0])
        self.play(Create(card), run_time=0.7)
        self.play(FadeIn(a_lab, shift=DOWN * 0.2), FadeIn(a_val, scale=0.85), run_time=0.8)
        self.wait(2.0)
