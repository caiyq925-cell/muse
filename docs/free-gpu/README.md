# 免费 GPU 生图 / 生视频说明：Colab + Kaggle

> 日期：2026-11-08
> 适用人：没有本地 GPU、不绑卡、没有外国手机号，用 Google 账号 `caiyq925@gmail.com`
> 状态：Colab 已实测跑通 SDXL；Kaggle 已注册登录，但手机验证未通过，GPU 尚未解锁（见第 2 节）
> 仓库：`caiyq925-cell/muse`，本文档在 `docs/free-gpu/README.md`

## 0. 一句话结论

- **现在就能用的：Google Colab 免费版。** 不用绑卡、不用手机验证，T4 显卡跑 SDXL 1024 图约 29 秒，已实测。
- **主力备选：Kaggle。** 每周 30 小时 GPU 额度，比 Colab 稳，但要先通过手机验证；2026-11-08 实测：填了本人 +86 手机号后 Kaggle 未发短信，直接要求走 Persona 身份验证（身份证件），尚未决定是否继续。
- **不要碰的：Modal。** 每月 $30 额度是真的，但官方计费文档要求必须有付款方式在档才能用，跟“不绑卡”冲突。
- **成片不用常驻服务：** 生成完下载到本地 / 手机，再去剪映里拼就行，不需要固定外网地址、不需要 24 小时在线。

## 1. 两个渠道对比

|  | Google Colab（免费） | Kaggle（免费） | Modal（已排除） |
|---|---|---|---|
| 费用 | $0，不绑卡 | $0，不绑卡 | Starter $0 + 每月 $30 额度，但必须有付款方式在档 |
| 注册 / 登录 | Google 账号直接开 | Google 账号注册，需手机验证 | 需付款方式 |
| GPU | 免费一般是 Tesla T4，16GB 显存 | T4 x2（两张 16GB T4），单次用一张；另有 TPU v3-8 | T4 / L4 / A10 / A100 / H100 等，按秒计费 |
| 每周 GPU 时间 | 约 15–30 小时，不固定，看平台需求 | 30 小时/周，写明的固定额度；TPU 另有 20 小时/周 | 每月 $30 额度，约 27 小时 T4 |
| 单次最长 | 12 小时，90 分钟不动就断 | 12 小时（TPU 9 小时），空闲约 20 分钟就断 | 按秒计费，用多久算多久 |
| 稳定性 | 额度不固定，高峰可能分不到 GPU | 额度稳，但高峰要排队；会话一断就没了 | 计费稳，但要绑卡 |
| 适合 | 随手测一张、玩 ComfyUI 界面 | 批量出图、固定时长的实验 | 不适合本方案 |
| 不适合 | 当服务器、24 小时在线 | 当服务器、对外提供 API（条款禁 server farming） | — |

## 2. 实测记录（2026-11-08）

### Colab：SDXL 已跑通

- 时间：2026-11-08 20:11，账号 `caiyq925@gmail.com`，浏览器已保存登录态直接进入，未触发手机验证。
- GPU：`nvidia-smi` 确认 Tesla T4，显存 15360 MiB。
- 笔记本：`sdxl_test.ipynb`（本目录同名文件），3 个代码格全部跑通。
  - 装 `diffusers` 等依赖：8.2 秒。
  - 加载 `stabilityai/stable-diffusion-xl-base-1.0`（fp16）：124.7 秒，下载 7.11GB（19 个文件）。
  - 生成：29.2 秒（30 步，约 23 秒推理），输出 `Saved sdxl_test.png (1024x1024)`。
- 成图：水彩绘本风，奶奶穿绿开衫、孩子穿橙色裙子，围着木桌分橘子，桌上和地上都有橘子。
- 关闭：跑完立即“断开连接并删除运行时”，页面变回“重新连接 T4”，GPU 已释放，不再空转。
- 成图文件在本地：`~/workspace/your_files/sdxl_test.png`（1.5MB，1024×1024）。

### Kaggle：已注册，未解锁

- 注册：2026-11-08 20:29，Google 账号 `caiyq925@gmail.com` 走 Google 注册。
- 用户名：Kaggle 只允许字母和数字，不允许连字符，最终为 `caiyq925cell`（不是 `caiyq925-cell`），账号编号 37810612。未设 Kaggle 密码、未绑卡、未付费。
- 额度：Settings 核查 GPU 30 小时/周，已用 00:00；TPU 20 小时/周，已用 00:00。
- 手机验证：2026-11-08 20:35，填了本人 +86 手机号、通过 reCAPTCHA、点了 Start verification 后，**Kaggle 未发短信、未出验证码框**，直接弹 `Identity verification required：无法用这个电话号码验证您，下一步需要验证您的身份`，要求走 Persona 第三方身份验证（通常涉及身份证件）。已停下，未重发、未绕过。
- 待用户决定：走 Persona、换个手机号再试，还是先放一放用 Colab。**在验证通过前，Kaggle 跑不了笔记本、开不了 GPU。**

### Modal：已排除

- 官网定价：Starter $0，每月 $30 免费额度。
- 官方计费文档原文：`you must have a payment method on file in order to use Modal`。第三方文章常只说“不用卡”，是误导。

## 3. Colab 怎么用

Colab 本质是云端 Jupyter 笔记本，代码跑在 Google 的服务器上，不是你的电脑。

1. 打开 <https://colab.research.google.com>，用 Google 账号登录，点“新建笔记本”。
2. 改 GPU：菜单 `Runtime（运行时）→ Change runtime type（更改运行时类型）→ Hardware accelerator → T4 GPU → Save`。
3. 先验卡：跑一格 `!nvidia-smi`，看到 Tesla T4 再往下跑；如果显示没有 GPU，说明当时分不到，等低峰再试，不要反复刷。
4. 按顺序跑代码格：装依赖 → 下模型 → 生成 → 保存。模型第一次下载要几分钟，SDXL base 约 6.9GB。
5. 保存成片：**文件存在 `/content/`，关了就没了。** 生成后立即下载，或存到 Google Drive（`drive.mount('/content/drive')`）。
6. 关 GPU：右上角运行时菜单 → `Disconnect and delete runtime（断开并删除运行时）`。确认按钮变回“重新连接”才算关了。

注意：

- 免费额度不保证，高峰分不到 GPU 是正常的；用多了会被限 GPU 一天左右。
- 每次重开都是新机器，装过的包、下载的模型都要重装重下；把安装命令放在笔记本最前面。
- 不要升级 Colab Pro，不要绑卡。

本目录的笔记本：

- `sdxl_test.ipynb`：已在 Colab 实测跑通的 SDXL 测试，提示词是水彩风奶奶和孙子分橘子。
- `comfyui_colab.ipynb`：ComfyUI + SDXL 草稿，未实测，见第 5 节。

## 4. Kaggle 怎么用

1. 打开 <https://www.kaggle.com>，点 Sign Up → `Register with Google`，选 `caiyq925@gmail.com`，用户名只能用字母和数字。
2. 去 `Account > Settings`，看手机验证状态和 GPU 额度。
3. 手机验证：点 Phone verify，填本人 +86 手机号（不可为公共或共享号码），收短信码填入。**注意：2026-11-08 实测该号未收到短信，直接被要求走 Persona 身份验证，见第 2 节。**
4. 验证通过后，在 <https://www.kaggle.com/code> 新建笔记本，右侧设置里选 `Accelerator → GPU T4 x2`，打开 `Internet`（下载模型要用）。
5. 上传 / 粘贴笔记本代码，运行，成片保存在 `/kaggle/working`（20GB），跑完下载到本地。
6. 关 GPU：结束会话，不要让它空转。单次最长 12 小时，空闲约 20 分钟会断。

注意：

- Kaggle 额度是每周 30 小时 GPU，1 小时 T4 x2 只扣 1 小时额度。
- Kaggle 条款禁 server farming / 对外提供服务，只能自己做实验、批量生成、下载走人。
- 一个手机号只能验证一个 Kaggle 账号，不要用公共号。

## 5. ComfyUI 能在 Colab 上部署吗？能

- 能。ComfyUI 是 2026 年扩散模型的标准节点式前端，支持 SDXL、Flux、Wan 2.2、LTX-Video 等。
- 免费 T4 够跑 SDXL 1024 图，约 25–40 秒一张；首次搭建约 8–12 分钟。
- 做法：克隆 ComfyUI → 装依赖 → 下 SDXL 模型到 `models/checkpoints/` → 后台起 `python main.py --listen --port 8188` → 用 cloudflared 开隧道，拿到 `*.trycloudflare.com` 链接，在浏览器里打开就是 ComfyUI。
- 隧道链接无鉴权，不要公开分享；会话一断链接就失效。
- **但不一定需要 ComfyUI：** 如果只是批量出图，用 diffusers 笔记本直接跑更快；ComfyUI 适合要调工作流、接 LoRA / ControlNet / 视频节点的时候用。
- 本目录 `comfyui_colab.ipynb` 是草稿，未实测，跑之前先看里面的步骤。

## 6. 能部署的最顶级模型是什么？（免费 T4，16GB 显存的天花板）

先说天花板：**免费 T4 跑不了 FLUX.1 Dev 原版 FP16（约 24GB）、Wan 14B FP16（24GB+）、Wan 2.7（约 27B）、Qwen-Image 20B，也跑不了 Midjourney / Sora / Kling 这类闭源商用模型。** 下面是 T4 上真正能跑、且在 2026 年算顶级的。

### 生图：推荐顺序

| 排名 | 模型 | 参数 / 显存 | 许可证 | 适合 | 备注 |
|---|---|---|---|---|---|
| 1（已实测，最稳） | **SDXL base 1.0** | 3.5B，8GB 起，12GB 舒服 | CreativeML Open RAIL++-M，商用允许 | 故事插画、LoRA、ControlNet、改图 | 生态最深，Civitai 上有几万个微调版和 LoRA；画质已不是 2026 年第一，但最稳 |
| 2（画质更好） | **FLUX.2 [klein] 4B** | 4B，约 13GB FP16，4 步出图 | Apache 2.0，商用允许 | 高质量出图、参考图编辑 | 2026-01 发布，从 FLUX.2 32B 蒸馏而来；Klein 9B 是非商用、要 27–29GB，别选 |
| 2（画质更好） | **Z-Image-Turbo** | 6B，16GB 内，8–9 步 | Apache 2.0 | 快速高质量出图、中英文文字 | 阿里通义 2025-11 发布，2026 年 16GB 卡的默认推荐之一 |
| 3（画质最高，需量化） | **FLUX.1 Dev GGUF Q8** | 12B，原版约 24GB，Q8 量化后可进 16GB | 非商用，商用需付费许可 | 非商用高质量出图、可读文字 | 原版 FP16 装不下；Q8 画质接近原版 |
| 备选 | SD 3.5 Large / Medium | 8.1B / 2.5B，FP8 约 11GB | Stability Community | 文字渲染、复杂构图 | 不是首选 |

**给本项目的建议：** 先用 SDXL（已跑通，风格 LoRA 最多，最适合水彩故事插画），下一步试 FLUX.2 Klein 4B 或 Z-Image-Turbo，看画质是否明显更好，再决定要不要换主力。

### 生视频：推荐顺序

| 排名 | 模型 | 参数 / 显存 | 许可证 | 适合 | 备注 |
|---|---|---|---|---|---|
| 1（画质） | **Wan 2.2 5B** | 5B，6–8GB，480p，约 5 秒/段 | Apache 2.0，商用无限制 | 文生视频 / 图生视频，故事动效片段 | 开源视频质量标杆，VBench 约 84.7%；T4 上最稳的选择 |
| 1（速度 / 有声） | **LTX-Video 0.9.5 / LTX-2** | LTX-2 约 22B，量化后 12GB 起；0.9.5 更轻 | LTX Community License，年收入 $10M 以下商用免费 | 快速迭代、带同步音频的片段 | LTX-2 是首个单次生成同步音视频的开源模型；0.9.5 在 T4 上约 6–8 分钟/段 |
| 2 | **Wan 2.2 14B GGUF Q4/Q5** | 14B，量化后可进 16GB，720p | Apache 2.0 | 更高画质的图生视频 | 原版 FP16 要 24GB+；GGUF 版在 Colab T4 上约 18 分钟/段，慢 |
| 3 | **CogVideoX 5B（量化）** | 5B，量化后 12GB | Apache 2.0 | 入门视频生成 | 最容易上手，但画质不如 Wan 2.2 |
| 不推荐 | HunyuanVideo 13B | 13B，24GB+ FP16 | 许可证排除欧盟、英国、韩国 | — | 画质电影感强，但许可证和显存都不适合 |
| 跑不动 | Wan 2.7 | 约 27B MoE，1080p、15 秒、原生音频 | 待核实 | — | 2026-04 报道的新旗舰，T4 装不下，不要按它规划 |

**给本项目的建议：** 视频不要指望一次出整条成片。正确流程是：SDXL 出一张静帧 → Wan 2.2 5B 图生视频，做成 4–6 秒动 clip → 下载 MP4 到本地 → 在剪映里拼。T4 上一个短片段要 10–30 分钟，是正常的。数学 / 精确动画继续用 Box 上的 Manim，AI 视频只做故事里的动效片段。

## 7. 外网 / 接出来用：和 Box 不一样

- **Box：** 没有公网入站，从外部连不进去；文件只能走网盘或 GitHub 中转，代码、渲染、验收都在 Box 里面闭环。
- **Colab / Kaggle：** 能接出来，但只是临时链接。
  - 出网：本来就能下载 Hugging Face 模型，也能把成片传到 Google Drive。
  - 入网：用 cloudflared（`*.trycloudflare.com`）、Gradio `--share`（`*.gradio.live`，有效 72 小时）、LocalTunnel 等隧道，把笔记本里的 localhost 端口暴露成公网链接，手机浏览器点开就能操作。
  - 临时：会话一断（Colab 最长 12 小时，Kaggle 约 9–12 小时），隧道就死了，下次重跑要换新链接；除非自己有域名建命名隧道，否则没有固定地址。
  - 不能当服务器：不能 24 小时在线接单，Kaggle 还明确禁 server farming。
- **用户已定：2026-11-08，成片有链接下载到本地就行，不需要常驻外网服务 / 固定隧道。** 所以本方案不建隧道服务器，只做“跑一批 → 下载 → 关 GPU”。

## 8. 成本与红线

- 全程 $0：不绑卡、不付费、不升级 Colab Pro / Kaggle 付费档。
- 注册、验证、付费前先问用户；遇到绑卡、扣费、授权时停下等确认，不要自动付款。
- 登录一次只做一个；Google 手机验证要先读清页面数字再点，点错数字会被锁几小时，不要反复试。
- 手机号、验证码、密码不要写进文档、不要发到公开处；本文档不含任何密码、验证码、手机号。
- 模型许可证要先看：商用前确认该模型的许可证（上表已标），FLUX.1 Dev、Klein 9B、Hunyuan 等有非商用或地域限制，别直接商用。
- 视频号 / 抖音发布前，按 2026-11-06 清朗要求做 AI 生成 + 虚构演绎双标注（本仓库 Manim 视频已有相关记录）。

## 9. 常见问题

- **分不到 GPU：** 高峰正常，等低峰再试；Colab 换 Kaggle（验证通过后）互为备份。
- **会话断了：** 正常，文件在 `/content/` / `/kaggle/working` 之外的都没了；成片要先下载或存 Drive，笔记本要能重跑。
- **模型下载慢 / 失败：** 第一次下 SDXL 约 7GB，要几分钟；失败就重跑下载那格，不要换模型。
- **Kaggle 手机验证失败：** 2026-11-08 实测：填号后未发短信，直接要求 Persona 身份验证。不要反复重发；决定走 Persona、换号，还是先用 Colab。
- **显存不够（OOM）：** 换更小的模型 / 量化版，降低分辨率（视频先用 480p），不要硬上 14B FP16。

## 10. 来源

- Modal 定价：<https://modal.com/pricing>；Modal 计费文档：<https://modal.com/docs/guide/billing>（“must have a payment method on file”）
- Kaggle 笔记本与 GPU 用量：<https://www.kaggle.com/docs/notebooks>、<https://www.kaggle.com/docs/efficient-gpu-usage>
- Colab 常见问题：<https://research.google.com/colaboratory/faq.html>
- SDXL：`stabilityai/stable-diffusion-xl-base-1.0`（Hugging Face）
- FLUX.2 Klein、Z-Image-Turbo、Wan 2.2、LTX-2：以各模型 Hugging Face 模型卡与许可证为准，版本变化快，商用前再核对一次。

## 11. 待办

- [ ] Kaggle：决定是否走 Persona 身份验证 / 换号，解锁 GPU 后在 Kaggle 跑一次 SDXL 对比 Colab。
- [ ] 生图：试 FLUX.2 Klein 4B 或 Z-Image-Turbo，对比 SDXL 的水彩故事风格。
- [ ] 生视频：在 Colab 试 Wan 2.2 5B 480p 图生视频（用已生成的 SDXL 图做首帧），下载 MP4 验收。
- [ ] ComfyUI：实测 `comfyui_colab.ipynb`，确认隧道链接可用。
