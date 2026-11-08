"""
智能客服满意度问题 —— ManimCE 竖屏讲解动画 v2（1080×1920，50~60 秒）
v1 基础上的修订版：竖屏重排版 + 修第 4 幕标题压算式 + 第 3 幕粉块真平移
+ 补 1+1/4=5/4 半步 + 第 5 幕真分数排版 + 烧录字幕（配音待补，见同名 .srt）
数学：3/5 × 6/5 = 18/25；18/25 × (1+1/4) = 18/25 × 5/4 = 90/100 = 9/10
渲染（Box 内）：~/manim-venv/bin/python -m manim render -qm -r 1080,1920 --format=mp4 smart_service_satisfaction_v2.py SmartServiceSatisfaction
时间轴（总长 56.0 秒；字幕换行点与同名 .srt 一致）：
  幕 1  0.0–6.0   钩子 + 题目
  幕 2  6.0–14.0  建模型
  幕 3 14.0–31.0  关键一跳（粉块从末格脱离、平移到末端落位变新增段）
  幕 4 31.0–41.0  列式求解（含 1+1/4=5/4 半步）
  幕 5 41.0–49.0  验算
  幕 6 49.0–56.0  答案卡 + 互动
"""
from manim import *
from fractions import Fraction

# ---------- 配色（同一颜色全片只表达同一意思） ----------
BG     = "#0B1026"   # 深色背景
C_COND = "#00D9FF"   # 青：条件
C_KEY  = "#FFC24B"   # 黄：关键一跳与最终答案
C_CHG  = "#FF6B9D"   # 粉：新增的那一段（全片只表达这一个意思）
C_OK   = "#2ED3A6"   # 绿：验算通过
C_TXT  = "#FFFFFF"   # 白：正文
C_SEC  = "#A9B4D8"   # 灰蓝：次要说明
CJK    = "Noto Sans CJK SC"

config.background_color = BG
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30
config.frame_width = 9
config.frame_height = 16

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

AX_L, AX_R, AY = -4.0, 4.0, 0.6   # 0~1 标尺（横向全宽）
AX_W = AX_R - AX_L
BAR_H = 0.7
SUB_Y = -5.35                      # 字幕中心：距底部约 18% 高度


def fr(x):
    """MathTex 用分数串"""
    return r"\frac{%d}{%d}" % (x.numerator, x.denominator)


def rich(parts, t_size=32, m_size=38, weight=None):
    """图文混排一行：parts 为 (kind, content, color)，kind 't' 文本 / 'm' 分数"""
    ms = []
    for kind, content, color in parts:
        if kind == 't':
            kw = dict(font=CJK, font_size=t_size, color=color)
            if weight is not None:
                kw["weight"] = weight
            ms.append(Text(content, **kw))
        else:
            ms.append(MathTex(content, font_size=m_size, color=color))
    return VGroup(*ms).arrange(RIGHT, buff=0.10)


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


def make_step(txt):
    """左上角步骤小药丸标签"""
    t = Text(txt, font=CJK, font_size=30, color=C_SEC)
    w = t.width + 0.55
    rect = RoundedRectangle(
        width=w, height=0.62, corner_radius=0.31,
        stroke_color=C_SEC, stroke_width=2,
        fill_color=BLACK, fill_opacity=0.35,
    )
    g = VGroup(rect, t)
    g.move_to([-4.5 + 0.12 + w / 2, 5.45, 0])
    return g


def make_sub(lines):
    """烧录字幕：lines 为 [(text, key_or_None), ...]，每行不超过 16 字，关键词标黄；
    黑色半透明底衬在画面下方（距底部约 18% 高度处），只占底部安全区。"""
    rows = []
    for text, key in lines:
        if key and key in text:
            i = text.find(key)
            segs = []
            if i > 0:
                segs.append(Text(text[:i], font=CJK, font_size=34, color=C_TXT))
            segs.append(Text(key, font=CJK, font_size=34, color=C_KEY, weight=BOLD))
            if i + len(key) < len(text):
                segs.append(Text(text[i + len(key):], font=CJK, font_size=34, color=C_TXT))
            rows.append(VGroup(*segs).arrange(RIGHT, buff=0))
        else:
            rows.append(Text(text, font=CJK, font_size=34, color=C_TXT))
    body = VGroup(*rows).arrange(DOWN, buff=0.14)
    bg = SurroundingRectangle(body, color=BLACK, fill_color=BLACK,
                              fill_opacity=0.5, buff=0.2, corner_radius=0.12)
    g = VGroup(bg, body)
    g.move_to([0, SUB_Y, 0])
    return g


def mkbox(tex_str, color, font_size=40):
    """幕 2 链条中的方框"""
    rect = RoundedRectangle(
        width=1.3, height=1.0, corner_radius=0.16,
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
    lab0 = Text("0", font=CJK, font_size=22, color=C_SEC).next_to(ax.get_start(), DOWN, buff=0.18)
    lab1 = Text("1", font=CJK, font_size=22, color=C_SEC).next_to(ax.get_end(), DOWN, buff=0.18)
    return VGroup(ax, ticks, lab0, lab1)


def ghost_line(x):
    """旧位置的粉色虚线残影"""
    return DashedLine([x, AY, 0], [x, AY + 0.85, 0],
                      dash_length=0.14, stroke_width=2.5, color=C_CHG)


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

        title = Text("智能客服满意度问题", font=CJK, font_size=54, color=C_TXT)
        title.move_to([0, 6.35, 0])
        self.sub = make_sub([("满意度只有五分之三，", None)])
        self.add(title, self.sub)

        # ==================== 幕 1 · 钩子 + 题目（0.0–6.0） ====================
        s1 = make_step("第 1 步 · 看题目")
        self.play(FadeIn(s1, shift=DOWN * 0.2), run_time=0.5)

        hook1 = rich([('t', "满意度只有 ", C_TXT), ('m', fr(F_ORIG), C_COND),
                      ('t', "，上了智能客服，", C_TXT)], 44, 50).move_to([0, 4.75, 0])
        hook2 = rich([('t', "居然能涨到 ", C_TXT), ('m', fr(F_ANS), C_KEY),
                      ('t', "？", C_TXT)], 44, 50).move_to([0, 3.95, 0])
        hook3 = rich([('t', "关键在", C_TXT), ('t', "第二个四分之一", C_KEY),
                      ('t', "。", C_TXT)], 44, 50).move_to([0, 3.15, 0])
        self.play(FadeIn(hook1, shift=UP * 0.2), FadeIn(hook2, shift=UP * 0.2),
                  FadeIn(hook3, shift=UP * 0.2), run_time=1.2)

        bar5 = cell_bar(5, F_ORIG.numerator, 1.15, 0.62, 0.06, C_COND)
        bar5.move_to([0, 1.9, 0])
        sub1 = make_sub([("上了智能客服，", None), ("居然能涨到十分之九？", None)])
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in bar5], lag_ratio=0.15),
                  FadeOut(self.sub), FadeIn(sub1), run_time=1.0)
        self.sub = sub1
        lab5 = rich([('m', fr(F_ORIG), C_COND), ('t', " 原来的满意度", C_SEC)],
                    30, 40).move_to([0, 1.0, 0])
        self.play(FadeIn(lab5), run_time=0.5)

        conds = VGroup(
            rich([('t', "① 客服人数少，满意度只有 ", C_COND), ('m', fr(F_ORIG), C_COND)], 32, 38),
            rich([('t', "② 智能客服单独服务：是原来的 ", C_COND), ('m', fr(R_AI), C_COND)], 32, 38),
            rich([('t', "③ 双重服务：满意度又提高了 ", C_COND), ('m', fr(R_UP), C_COND)], 32, 38),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        conds.move_to([-4.2 + conds.width / 2, -0.55, 0])
        sub2 = make_sub([("关键，就藏在", None), ("第二个四分之一里。", "第二个四分之一")])
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.4) for c in conds], lag_ratio=0.5),
                  FadeOut(self.sub), FadeIn(sub2), run_time=1.6)
        self.sub = sub2
        q = Text("那么，现在的满意度是多少？", font=CJK, font_size=40,
                 color=C_TXT, weight=BOLD).move_to([0, -3.0, 0])
        self.play(FadeIn(q, shift=RIGHT * 0.4), run_time=0.6)
        self.wait(0.6)

        # ==================== 幕 2 · 建模型（6.0–14.0） ====================
        s2 = make_step("第 2 步 · 建模型")
        sub3 = make_sub([("先别算。第一句话，", None),
                         ("是原来的五分之六，乘五分之六。", None)])
        self.play(FadeOut(conds), FadeOut(q), FadeOut(s1), FadeIn(s2),
                  FadeOut(hook1), FadeOut(hook2), FadeOut(hook3),
                  bar5.animate.move_to([0, 4.6, 0]),
                  lab5.animate.move_to([0, 3.7, 0]),
                  FadeOut(self.sub), FadeIn(sub3), run_time=0.5)
        self.sub = sub3

        box1 = mkbox(fr(F_ORIG), C_COND)
        box2 = mkbox("?", C_SEC)
        box3 = mkbox("?", C_SEC)
        a1 = Arrow(ORIGIN, RIGHT * 1.0, buff=0, stroke_width=5, color=C_COND)
        a2 = Arrow(ORIGIN, RIGHT * 1.0, buff=0, stroke_width=5, color=C_COND)
        row = VGroup(box1, a1, box2, a2, box3).arrange(RIGHT, buff=0.3)
        row.move_to([0, 1.6, 0])
        t1 = MathTex(r"\times", fr(R_AI), font_size=36, color=C_COND)
        t1.next_to(a1, UP, buff=0.12)
        t2 = MathTex(r"\times\left(1+", fr(R_UP), r"\right)", font_size=36, color=C_COND)
        t2.next_to(a2, UP, buff=0.12)
        chain = VGroup(row, t1, t2)
        self.play(LaggedStart(
            FadeIn(box1, scale=0.7),
            FadeIn(a1, shift=RIGHT * 0.3), FadeIn(t1, scale=0.7),
            FadeIn(box2, scale=0.7),
            FadeIn(a2, shift=RIGHT * 0.3), FadeIn(t2, scale=0.7),
            FadeIn(box3, scale=0.7),
            lag_ratio=0.22), run_time=3.0)
        note1 = rich([('t', "「是原来的 ", C_SEC), ('m', fr(R_AI), C_COND),
                      ('t', "」→ 乘 ", C_SEC), ('m', fr(R_AI), C_COND)],
                     30, 36).move_to([0, -0.6, 0])
        sub4 = make_sub([("第二句话，提高四分之一，", None),
                         ("就是乘一加四分之一。", None)])
        self.play(FadeIn(note1, shift=UP * 0.2),
                  FadeOut(self.sub), FadeIn(sub4), run_time=0.6)
        self.sub = sub4
        note2 = rich([('t', "「又提高 ", C_SEC), ('m', fr(R_UP), C_COND),
                      ('t', "」→ 乘（1+", C_SEC), ('m', fr(R_UP), C_COND),
                      ('t', "）", C_SEC)], 30, 36).move_to([0, -1.5, 0])
        warn = rich([('m', fr(R_AI), C_KEY), ('t', " 是跟原来比的倍数，", C_SEC),
                     ('t', "不是占总数的 ", C_SEC), ('m', fr(R_AI), C_KEY)],
                    28, 34).move_to([0, -2.5, 0])
        self.play(FadeIn(note2, shift=UP * 0.2), FadeIn(warn, shift=UP * 0.2), run_time=0.6)
        self.play(Indicate(t2, color=C_KEY, scale_factor=1.15), run_time=0.8)
        sub5 = make_sub([("注意：五分之六是倍数，", "五分之六"),
                         ("不是占总数的五分之六。", "五分之六")])
        self.play(FadeOut(self.sub), FadeIn(sub5), run_time=0.3)
        self.sub = sub5
        self.wait(2.2)

        # ==================== 幕 3 · 关键一跳（14.0–31.0） ====================
        s3 = make_step("第 3 步 · 关键一跳")
        sub6 = make_sub([("先看第一步，", None),
                         ("条从五分之三长到二十五分之十八。", None)])
        self.play(FadeOut(chain), FadeOut(note1), FadeOut(note2), FadeOut(warn),
                  FadeOut(bar5), FadeOut(lab5), FadeOut(s2), FadeIn(s3),
                  FadeOut(self.sub), FadeIn(sub6), run_time=0.5)
        self.sub = sub6

        axis = make_axis()
        self.play(Create(axis), run_time=0.7)
        f0, f1_, f2_ = float(F_ORIG), float(F_MID), float(F_ANS)
        x0 = AX_L + AX_W * f0       # 3/5 的位置
        x1 = AX_L + AX_W * f1_      # 18/25 的位置
        x2 = AX_L + AX_W * f2_      # 9/10 的位置

        barA = bar_at(f0)
        self.play(GrowFromEdge(barA, LEFT), run_time=0.6)
        labA = MathTex(fr(F_ORIG), font_size=44, color=C_COND)
        labA.next_to(barA, UP, buff=0.16, aligned_edge=RIGHT).shift(RIGHT * 0.18)
        self.play(FadeIn(labA), run_time=0.4)

        # 第一次放大：×6/5 —— 条本身变长，末端只用粉色描边标出新增部分
        g1 = ghost_line(x0)
        mul1 = rich([('t', "乘 ", C_COND), ('m', fr(R_AI), C_COND)],
                    30, 36).move_to([(x0 + x1) / 2, -0.4, 0])
        self.play(FadeIn(g1), FadeIn(mul1, shift=UP * 0.15), run_time=0.5)
        barB = bar_at(f1_)
        labB = MathTex(fr(F_MID), font_size=44, color=C_COND)
        labB.next_to(barB, UP, buff=0.16, aligned_edge=RIGHT).shift(RIGHT * 0.18)
        inc1 = RoundedRectangle(
            width=AX_W * (f1_ - f0), height=BAR_H, corner_radius=0.06,
            stroke_color=C_CHG, stroke_width=3, fill_opacity=0,
        ).move_to([(x0 + x1) / 2, AY + BAR_H / 2, 0])
        self.play(ReplacementTransform(barA, barB),
                  ReplacementTransform(labA, labB),
                  FadeIn(inc1), run_time=1.1)
        sub7 = make_sub([("现在看第二步，", None),
                         ("提高的四分之一，是对着谁算的？", None)])
        self.play(FadeOut(inc1), FadeOut(self.sub), FadeIn(sub7), run_time=0.5)
        self.sub = sub7

        # ⭐ 关键一跳：把 18/25 的条切成 4 等份，粉块是其中最后一份
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
        self.play(FadeIn(block, shift=UP * 0.3), run_time=0.45)
        labq = rich([('t', "这个 ", C_CHG), ('m', fr(R_UP), C_CHG)],
                    30, 36).move_to([x1 - w18 / 8, -0.45, 0])
        sub8 = make_sub([("是对着现在的二十五分之十八！", None)])
        self.play(FadeIn(labq), FadeOut(self.sub), FadeIn(sub8), run_time=0.4)
        self.sub = sub8
        punch1 = rich([('t', "单位「1」变了：这次的 ", C_KEY), ('m', fr(R_UP), C_KEY),
                       ('t', "，", C_KEY)], 34, 40, weight=BOLD).move_to([0, 3.75, 0])
        punch2 = rich([('t', "是 ", C_KEY), ('m', fr(F_MID), C_KEY),
                       ('t', " 的 ", C_KEY), ('m', fr(R_UP), C_KEY),
                       ('t', "，不是原来 ", C_KEY), ('m', fr(F_ORIG), C_KEY),
                       ('t', " 的 ", C_KEY), ('m', fr(R_UP), C_KEY),
                       ('t', "。", C_KEY)], 34, 40, weight=BOLD).move_to([0, 3.0, 0])
        self.play(FadeIn(punch1, shift=UP * 0.2), FadeIn(punch2, shift=UP * 0.2), run_time=0.8)
        self.wait(0.6)

        # 第二次放大：×5/4 —— 粉块从旧条末格脱离、平移到末端落位，变成新增段
        g2 = ghost_line(x1)
        mul2 = rich([('t', "乘 ", C_COND), ('m', fr(R_DUAL), C_COND)],
                    30, 36).move_to([(x1 + x2) / 2, -0.4, 0])
        self.play(FadeOut(labq), FadeIn(g2), FadeIn(mul2, shift=UP * 0.15), run_time=0.5)
        labC = MathTex(fr(F_ANS), font_size=52, color=C_KEY)
        labC.move_to([x2 - labC.width / 2 - 0.1, AY + BAR_H + 0.51, 0])
        sub9 = make_sub([("把它切成四份，其中一份，", None),
                         ("就是新长出来的这一段。", None)])
        self.play(block.animate.move_to([(x1 + x2) / 2, AY + BAR_H / 2, 0]),
                  barB.animate.set_stroke(color=C_COND, width=2.5),
                  ReplacementTransform(labB, labC),
                  FadeOut(splits),
                  FadeOut(self.sub), FadeIn(sub9), run_time=1.6)
        self.sub = sub9
        self.play(Indicate(labC, color=C_KEY, scale_factor=1.25), run_time=0.6)

        # 错答点名排除：拿原来 3/5 的 1/4 来算会错成 87/100（灰色小字 + 划掉）
        wrong = rich([('t', "如果拿原来 ", C_SEC), ('m', fr(F_ORIG), C_SEC),
                      ('t', " 的 ", C_SEC), ('m', fr(R_UP), C_SEC),
                      ('t', " 来算 → ", C_SEC),
                      ('m', r"\frac{87}{100}", C_SEC)],
                     30, 36).move_to([0, -1.6, 0])
        self.play(FadeIn(wrong, shift=UP * 0.15), run_time=0.5)
        strike = Line(wrong.get_left() + LEFT * 0.1 + UP * 0.05,
                      wrong.get_right() + RIGHT * 0.1 + UP * 0.05,
                      color="#FF5555", stroke_width=4)
        self.play(Create(strike), run_time=0.4)
        self.play(FadeOut(wrong), FadeOut(strike), run_time=0.5)
        self.wait(2.1)
        sub10 = make_sub([("拿原来五分之三的四分之一来算，", None),
                          ("就会错成一百分之八十七。", None)])
        self.play(FadeOut(self.sub), FadeIn(sub10), run_time=0.3)
        self.sub = sub10
        self.wait(2.7)
        stage3 = VGroup(axis, barB, labC, block, g1, g2, mul2, punch1, punch2)

        # ==================== 幕 4 · 列式求解（31.0–41.0） ====================
        s4 = make_step("第 4 步 · 列式求解")
        sub11 = make_sub([("列式就是两步：", None),
                          ("五分之三乘五分之六，", None)])
        self.play(FadeOut(stage3), FadeOut(s3), FadeIn(s4),
                  FadeOut(self.sub), FadeIn(sub11), run_time=0.6)
        self.sub = sub11
        eqs = VGroup(
            MathTex(fr(F_ORIG), r"\times", fr(R_AI), r"=", fr(F_MID), font_size=46),
            MathTex(fr(F_MID), r"\times\left(1+", fr(R_UP), r"\right)", font_size=46),
            MathTex(r"1+", fr(R_UP), r"=", r"\frac{4}{4}+\frac{1}{4}", r"=", fr(R_DUAL), font_size=46),
            MathTex(r"=", fr(F_MID), r"\times", fr(R_DUAL), font_size=46),
            MathTex(r"=", r"\frac{%d}{%d}" % (NUM10, DEN10), font_size=46),
            MathTex(r"=", fr(F_ANS), font_size=50),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        eqs.move_to([-4.5 + 0.3 + eqs.width / 2, 0.95, 0])
        eqs[0][0].set_color(C_COND); eqs[0][2].set_color(C_COND); eqs[0][4].set_color(C_KEY)
        eqs[1][0].set_color(C_KEY); eqs[1][2].set_color(C_COND)
        eqs[2][1].set_color(C_COND); eqs[2][5].set_color(C_KEY)
        eqs[3][1].set_color(C_KEY); eqs[3][3].set_color(C_COND)
        eqs[4][1].set_color(C_KEY)
        eqs[5][1].set_color(C_KEY)
        for i, e in enumerate(eqs):
            if i == 2:
                sub12 = make_sub([("得二十五分之十八。", None),
                                  ("一加四分之一等于四分之五，", None)])
                self.play(FadeIn(e, shift=RIGHT * 0.35),
                          FadeOut(self.sub), FadeIn(sub12), run_time=0.6)
                self.sub = sub12
            elif i == 4:
                sub13 = make_sub([("再乘上去，百分之九十，", None),
                                  ("约分得十分之九。", None)])
                self.play(FadeIn(e, shift=RIGHT * 0.35),
                          FadeOut(self.sub), FadeIn(sub13), run_time=0.6)
                self.sub = sub13
            else:
                self.play(FadeIn(e, shift=RIGHT * 0.35), run_time=0.6)
            self.wait(0.5)
        note2 = Text("另法：0.6 ×1.2=0.72，×1.25=0.9", font=CJK, font_size=26, color=C_SEC)
        note2.move_to([-4.2 + note2.width / 2, -2.9, 0])
        self.play(FadeIn(note2), run_time=0.5)
        self.wait(2.3)

        # ==================== 幕 5 · 验算（41.0–49.0） ====================
        s5 = make_step("第 5 步 · 代回验算")
        sub14 = make_sub([("验算一下：", None),
                          ("十分之九除以四分之五，", None)])
        self.play(FadeOut(eqs), FadeOut(note2), FadeOut(s4), FadeIn(s5),
                  FadeOut(self.sub), FadeIn(sub14), run_time=0.5)
        self.sub = sub14
        bar10 = cell_bar(10, F_ANS.numerator, 0.68, 0.62, 0.05, C_OK)
        bar10.move_to([0, 3.6, 0])
        lab10 = MathTex(fr(F_ANS), font_size=44, color=C_OK).move_to([0, 4.55, 0])
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in bar10], lag_ratio=0.1),
                  run_time=1.1)
        nums = VGroup(*[
            Text(str(i + 1), font=CJK, font_size=15, color=C_SEC)
            .move_to([c.get_x(), 3.05, 0])
            for i, c in enumerate(bar10)
        ])
        self.play(FadeIn(nums), FadeIn(lab10), run_time=0.5)

        r1 = VGroup(
            MathTex(fr(F_ANS), r"\div", fr(R_DUAL), r"=", fr(F_MID), font_size=36, color=C_TXT),
            Text("　回到双重服务前", font=CJK, font_size=28, color=C_SEC),
            MathTex(r"\checkmark", font_size=36, color=C_OK),
        ).arrange(RIGHT, buff=0.25)
        r1.move_to([-4.2 + r1.width / 2, 1.9, 0])
        r2 = VGroup(
            MathTex(fr(F_MID), r"\div", fr(R_AI), r"=", fr(F_ORIG), font_size=36, color=C_TXT),
            Text("　回到最初的满意度", font=CJK, font_size=28, color=C_SEC),
            MathTex(r"\checkmark", font_size=36, color=C_OK),
        ).arrange(RIGHT, buff=0.25)
        r2.move_to([-4.2 + r2.width / 2, 0.75, 0])
        r3 = VGroup(
            MathTex(fr(F_ANS), font_size=36, color=C_TXT),
            Text(" 没超过 1，在 0~1 标尺内，合理", font=CJK, font_size=28, color=C_TXT),
            MathTex(r"\checkmark", font_size=36, color=C_OK),
        ).arrange(RIGHT, buff=0.25)
        r3.move_to([-4.2 + r3.width / 2, -0.4, 0])
        self.play(FadeIn(r1, shift=UP * 0.15), run_time=0.6)
        sub15 = make_sub([("回到双重服务前；", None),
                          ("再除以五分之六，", None)])
        self.play(Indicate(r1[-1], color=C_OK, scale_factor=1.4),
                  FadeOut(self.sub), FadeIn(sub15), run_time=0.5)
        self.sub = sub15
        self.play(FadeIn(r2, shift=UP * 0.15), run_time=0.6)
        self.play(Indicate(r2[-1], color=C_OK, scale_factor=1.4), run_time=0.5)
        sub16 = make_sub([("回到最初的五分之三，", None),
                          ("都对上了。", None)])
        self.play(FadeIn(r3, shift=UP * 0.15),
                  FadeOut(self.sub), FadeIn(sub16), run_time=0.6)
        self.sub = sub16
        self.play(Indicate(r3[-1], color=C_OK, scale_factor=1.4), run_time=0.5)
        self.wait(2.6)

        # ==================== 幕 6 · 答案卡 + 互动（49.0–56.0） ====================
        sub17 = make_sub([("记住这个办法：", None),
                          ("看到「又提高几分之几」，", None)])
        self.play(*[FadeOut(m) for m in (title, s5, bar10, nums, lab10, r1, r2, r3)],
                  FadeOut(self.sub), FadeIn(sub17), run_time=0.7)
        self.sub = sub17
        card = RoundedRectangle(
            width=8.2, height=3.0, corner_radius=0.35,
            stroke_color=C_KEY, stroke_width=4,
            fill_color=C_TXT, fill_opacity=0.04,
        ).move_to([0, 1.3, 0])
        a_lab = Text("答案", font=CJK, font_size=26, color=C_SEC).move_to([0, 2.3, 0])
        a_val = VGroup(
            Text("现在的满意度是 ", font=CJK, font_size=44, color=C_KEY, weight=BOLD),
            MathTex(fr(F_ANS), font_size=60, color=C_KEY),
        ).arrange(RIGHT, buff=0.22).move_to([0, 1.3, 0])
        self.play(Create(card), run_time=0.7)
        self.play(FadeIn(a_lab, shift=DOWN * 0.2), FadeIn(a_val, scale=0.85), run_time=0.8)
        koujue1 = Text("方法口诀：单位「1」变了没有？", font=CJK, font_size=32, color=C_TXT)
        koujue1.move_to([0, -1.0, 0])
        koujue2 = Text("先看提高是对着谁算的。", font=CJK, font_size=32, color=C_TXT)
        koujue2.move_to([0, -1.7, 0])
        sub18 = make_sub([("先问一句，是对着谁提高的。", None)])
        self.play(FadeIn(koujue1, shift=UP * 0.15), FadeIn(koujue2, shift=UP * 0.15),
                  FadeOut(self.sub), FadeIn(sub18), run_time=0.6)
        self.sub = sub18
        hudong1 = rich([('t', "如果第二句话改成「提高了 ", C_TXT),
                        ('m', fr(Fraction(1, 5)), C_TXT),
                        ('t', "」，答案是多少？", C_TXT)], 32, 38).move_to([0, -2.9, 0])
        hudong2 = Text("评论区试试", font=CJK, font_size=32, color=C_KEY, weight=BOLD)
        hudong2.move_to([0, -3.6, 0])
        self.play(FadeIn(hudong1, shift=UP * 0.15), FadeIn(hudong2, shift=UP * 0.15), run_time=0.6)
        sub19 = make_sub([("单位「1」找对了，", None),
                          ("题就做对了一大半。", None)])
        self.play(Indicate(a_val, color=C_KEY, scale_factor=1.1),
                  FadeOut(self.sub), FadeIn(sub19), run_time=0.8)
        self.sub = sub19
        self.wait(2.8)
