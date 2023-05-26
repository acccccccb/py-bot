<template>
    <div>
        <pre>{{ gamepad }}</pre>
        <pre>{{ dogTop }}</pre>
        <pre>{{ dogLeft }}</pre>
        <pre>{{ dogTop2 }}</pre>
        <pre>{{ dogLeft2 }}</pre>
        <pre>{{ lock }}</pre>
        <div class="dog" :style="{
            top: dogTop + 'px',
            left: dogLeft + 'px'
        }"></div>
        <div class="dog" :style="{
            top: dogTop2 + 'px',
            left: dogLeft2 + 'px'
        }"></div>
        <img style="display: block;-webkit-user-select: none;margin: auto;background-color: hsl(0, 0%, 25%);"
            src="http://127.0.0.1:8899/video_feed">
        <video controls autoplay width="800" height="600" src="http://127.0.0.1:8899/video_feed"></video>
        <div class="gamepad-main"
            :class="gamepad.left_tigger_value !== -1 && gamepad.right_tigger_value !== -1 ? 'bamepad-main-active' : ''">
            <template v-if="btnVisible">
                <div class="flex gamepad">
                    <div>
                        <button :disabled="gamepad.btn !== 9">L1</button>
                        <button :disabled="gamepad.left_tigger_value === -1">L2</button>
                    </div>
                    <div>
                        <button :disabled="gamepad.right_tigger_value === -1">R2</button>
                        <button :disabled="gamepad.btn !== 10">r1</button>
                    </div>
                </div>
                <div class="flex gamepad">
                    <div style="text-align: center;">
                        <div>
                            <button :disabled="gamepad.btn !== 11">上</button>
                        </div>
                        <div>
                            <button :disabled="gamepad.btn !== 13" style="margin-right: 20px;">左</button>
                            <button :disabled="gamepad.btn !== 14" style="margin-left: 20px;">右</button>
                        </div>
                        <div>
                            <button :disabled="gamepad.btn !== 12">下</button>
                        </div>
                    </div>
                    <div style="margin-top: 20px">
                        <button :disabled="gamepad.btn !== 4" style="margin-right: 10px;">Select</button>
                        <button :disabled="gamepad.btn !== 6" style="margin-left: 10px;">Start</button>
                    </div>
                    <div style="text-align: center;">
                        <div>
                            <button :disabled="gamepad.btn !== 2">X</button>
                        </div>
                        <div>
                            <button :disabled="gamepad.btn !== 3" style="margin-right: 20px;">Y</button>
                            <button :disabled="gamepad.btn !== 0" style="margin-left: 20px;">A</button>
                        </div>
                        <div>
                            <button :disabled="gamepad.btn !== 1">B</button>
                        </div>
                    </div>
                </div>
                <div class="flex gamepad">
                    <div>
                        <button :disabled="gamepad.btn !== 15">⭐</button>
                    </div>
                    <div>
                        <button :disabled="gamepad.btn !== 5">🏠</button>
                    </div>
                </div>
            </template>
            <div class="flex gamepad">
                <div class="left_axis">
                    <div class="left_axis_btn" :class="gamepad.btn === 7 ? 'axis_btn_press' : ''" :style="{
                        left: gamepad.left_axis_x * 50 + 50 + 'px',
                        top: gamepad.left_axis_y * 50 + 50 + 'px',
                    }"></div>
                </div>
                <div class="right_axis">
                    <div class="right_axis_btn" :class="gamepad.btn === 8 ? 'axis_btn_press' : ''" :style="{
                        left: gamepad.right_axis_x * 50 + 50 + 'px',
                        top: gamepad.right_axis_y * 50 + 50 + 'px',
                    }"></div>
                </div>
            </div>
            <div class="mouse" :class="gamepad.btn === -1 ? 'mouse-close' : ''"></div>
        </div>
    </div>
</template>
<script>
export default {
    name: "gamepad",
    data() {
        return {
            lock: false,
            btnVisible: false,
            gamepad: {
                "power_level": -1,
                "btn": -1,
                "left_tigger_value": -1,
                "right_tigger_value": -1,
                "left_axis_x": 0,
                "left_axis_y": 0,
                "right_axis_x": 0,
                "right_axis_y": 0
            },
            dogTop: 0,
            dogLeft: 0,
            dogTop2: 0,
            dogLeft2: 0,
        }
    },
    created() {
        this.websocketInit();
    },
    methods: {
        websocketInit() {
            const _this = this;
            // Create WebSocket connection.
            const socket = new WebSocket(`ws://${window.location.hostname}:8765`);

            // Connection opened
            socket.addEventListener("open", (event) => {
                socket.send("Hello Server!");
            });

            // Listen for messages
            socket.addEventListener("message", (event) => {
                const reader = new FileReader();

                // 将接收到的二进制数据转换为文本
                reader.onload = function () {
                    const text = reader.result;
                    const jsonData = JSON.parse(text);

                    // 在控制台中打印解析后的 JSON 数据
                    // console.log(jsonData);
                    _this.gamepad = jsonData;
                    _this.dogLeft += jsonData.left_axis_x * 50;
                    _this.dogTop += jsonData.left_axis_y * 50;
                    _this.dogLeft2 += jsonData.right_axis_x * 50;
                    _this.dogTop2 += jsonData.right_axis_y * 50;
                    // 进行其他操作
                    // ...
                };

                reader.readAsText(event.data);
            });
        }
    },
    watch: {
        'gamepad': {
            deep: true,
            handler: function () {
                if (this.gamepad.left_tigger_value !== -1 && this.gamepad.right_tigger_value !== -1) {
                    if (window.$lockTimmer) {
                        clearTimeout(window.$lockTimmer);
                    }
                    window.$lockTimmer = setTimeout(() => {
                        this.lock = false;
                    }, 100)
                    if (!this.lock) {
                        this.lock = true;
                        this.btnVisible = !this.btnVisible
                    }
                }
            }
        }
    }
}
</script>
<style scoped>
.gamepad-main {
    width: 400px;
    height: 350px;
    margin: auto;
    transform: translateY(25%);
    border: 1px solid #fff;
    padding: 40px;
    transition: all .5s;
}

.bamepad-main-active {
    background: goldenrod;
    transition: all .5s;
}

.mouse {
    width: 200px;
    height: 30px;
    margin: 20px auto;
    border: 1px solid #fff;
    transition: all .3s;
}

.mouse-close {
    height: 10px;
    transition: all .3s;
}

.gamepad {
    width: 100%;
}

.flex {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
}

.left_axis,
.right_axis {
    width: 100px;
    height: 100px;
    border: 1px solid #fff;
    position: relative;
    border-radius: 50%;
}

.left_axis_btn,
.right_axis_btn {
    width: 20px;
    height: 20px;
    position: absolute;
    background: #fff;
    transform: translate(-50%, -50%);
    transition: all 0.2s;
    border-radius: 50%;
}

.axis_btn_press {
    background: red;
}

.dog {
    position: fixed;
    width: 50px;
    height: 50px;
    background: rgb(112, 174, 255);
    transition: all 0.2s;
}
</style>