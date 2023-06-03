<script setup></script>
<template>
    <div>
        <div style="display: flex">
            <div class="canvas-box">
                <canvas id="canvas" :style="{
                        width: bitWidth * blockSize + 'px'
                    }"></canvas>
            </div>
            
        </div>
        <!-- <div>{{ isStart }}</div>
        <div>{{ speed }}</div>
        <div>{{ score }}</div>
        <div>{{ printData }}</div> -->
        <!-- <div>{{ lockData }}</div> -->
        {{ devicePixelRatio }}
        <button @click="editMode = !editMode">editMode</button>
        <button @click="createBlock">createBlock</button>
        <button @click="up(1, true)">up</button>
        <button @click="down(1, true)">down</button>
        <button @click="left(1, true)">left</button>
        <button @click="right(1, true)">right</button>
        <button @click="roll">roll</button>
        <button @click="saveToLockData">saveToLockData</button>
        <button @click="refreshScreen">refreshScreen</button>
        <button @click="start(true)">start</button>
        <button @click="speed+=1">speed +</button>
        <button @click="speed-=1">speed -</button>
        <button @click="lock = !lock">lock</button>
            <div v-if="editMode">
                <div class="main">
                    <div class="line" v-for="(item, y) in print" :key="y">
                        <div class="block" :class="o === '0' ? 'block-0' : 'block-1'" v-for="(o, x) in item" :key="x"
                            @click="blockOnClick(x, y)">
                        </div>
                    </div>
                </div>
                <div>{{ printData }}</div>
                <div>{{ lockData }}</div>
            </div>
    </div>
</template>
<script>
import * as _ from 'lodash'
export default {
    name: 'ArrayBlock',
    data() {
        return {
            ratio: 2,
            editMode: false,
            fps: 30,
            drawTimestamp: 0,
            drawTimmer: null,
            canvas: null,
            isStart: false,
            lock: false,
            bitWidth: 31, // max 31
            blockSize: 10,
            speed: 1,
            score: 0,
            printData: [],
            lockData: [],
            defaultLockDataFill: 2139095295,
            // defaultLockDataFill: 0,
            defaultLockDataFillItem: [],
            blocks: [
                // [ 0, 0, 0, 1996800, 2196480, 4194816, 9335040, 17926272, 35652672, 73818656, 76124448, 76402976, 126456288, 40265280, 43264320, 43264320, 39994944, 16875648, 8388864, 4194816, 4193280, 29889408, 35923008, 80890144, 156338832, 173115984, 72354336, 8388096, 4194816, 4194816, 4194816 ],
                // [ 0, 0, 0, 1996800, 2196480, 4194816, 9335040, 17926272, 35652672, 73818656, 76124448, 76263712, 126456288, 40265280, 43264320, 43264320, 39994944, 16875648, 8388864, 4194816, 4193280, 29889408, 35923008, 80890144, 156338832, 173115984, 72354336, 8388096, 4194816, 4194816, 4194816 ],
                // [8257536, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [98304, 49152, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [32768, 114688, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [98304, 98304, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [32768, 32768, 32768, 32768, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [65536, 98304, 32768, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [98304, 32768, 32768, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [49152, 32768, 32768, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [196608, 65536, 98304, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [32768, 98304, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        }
    },
    created() {
        this.resetPrintData();
        this.resetLockData();
        window.onkeydown = (e) => {
            if (e.keyCode === 37) {
                this.left(1, true)
            } else if (e.keyCode === 38) {
                this.roll(1, true)
            } else if (e.keyCode === 39) {
                this.right(1, true)
            } else if (e.keyCode === 40) {
                this.down(1, true)
            }
        }
    },
    mounted() { 
        this.initCanvas()
    },
    methods: {
        initCanvas() { 
            this.canvas = document.getElementById('canvas');
            this.canvas.width = this.bitWidth * this.blockSize * this.ratio;
            this.canvas.height = this.bitWidth * this.blockSize * this.ratio;
            this.drawOnCanvas()
            this.drawText()
        },
        drawRect(x, y, fill = true) { 
            const ctx = this.canvas.getContext("2d");
            ctx.fillStyle = fill ? "black" : "white"
            ctx.fillRect(x * this.ratio, y * this.ratio, this.blockSize * this.ratio, this.blockSize * this.ratio);
            if (fill) {
                ctx.strokeStyle = "white"
                ctx.lineWidth = 1 * this.ratio;
                ctx.strokeRect((x + 2) * this.ratio, (y + 2) * this.ratio, (this.blockSize - 4) * this.ratio, (this.blockSize - 4) * this.ratio);
            }
        },
        drawText() { 
            const ctx = this.canvas.getContext("2d");

            ctx.fillStyle = "white"
            ctx.fillRect(0, 0, this.blockSize * 8 * this.ratio, this.blockSize * this.bitWidth * this.ratio);
            ctx.fillRect(this.blockSize * (this.bitWidth - 8) * this.ratio, 0, this.blockSize * 8 * this.ratio, this.blockSize * this.bitWidth * this.ratio);

            ctx.strokeStyle = "black"
            ctx.lineWidth = 1;
            ctx.strokeRect(this.blockSize * 8 * this.ratio, 0, this.blockSize * (this.bitWidth - 16) * this.ratio, this.blockSize * this.bitWidth * this.ratio - 1);

            ctx.font = `${12 * this.ratio}px serif`;
            ctx.textAlign = "left";
            ctx.fillStyle = "black";
            ctx.fillText(`Speed: ${this.speed}`, 3 * this.ratio, 16 * 1 * this.ratio);
            ctx.fillText(`Score: ${this.score}`, 3 * this.ratio, 16 * 2 * this.ratio);
            ctx.fillText(`Fps: ${this.fps}`, 3 * this.ratio, 16 * 3 * this.ratio);
        },
        drawOnCanvas() {
            this.print.map((item, y) => { 
                item.forEach((childItem, x) => { 
                    this.drawRect(x * this.blockSize, y * this.blockSize, childItem === '1');
                })
            })
            this.drawRect(0 * this.blockSize, 0 * this.blockSize, true);
        },
        start(start) {
            if (this.lock || this.isStart) {
                return;
            }
            if (start) {
                this.isStart = true;
            }
            const loop = () => { 
                if (this.lockData.filter(item => item === this.defaultLockDataFill).length === 0) {
                    this.isStart = false;
                } else {
                    this.down(1, true)
                    if (!this.printData.find(item => !!item)) {
                        this.createBlock()
                    }
                    setTimeout(() => {
                        loop();
                    }, 1000 / this.speed)
                }
            }
            loop();
        },
        resetPrintData() {
            this.printData = new Array(this.bitWidth).fill(0)
        },
        resetLockData() {
            this.score = 0;
            this.lockData = new Array(this.bitWidth).fill(this.defaultLockDataFill)
            this.defaultLockDataFillItem = this.binary2Arr(this.lockData)[0]
        },
        saveToLockData() {
            const printData = this.binary2Arr(this.printData);
            let lockData = this.binary2Arr(this.lockData);
            printData.forEach((item, y) => {
                item.forEach((pix, x) => {
                    lockData[y][x] = lockData[y][x] === '1' ? lockData[y][x] : printData[y][x]
                })
            })
            lockData.forEach((item, index) => {
                if (item.filter(filterItem => filterItem === '0').length === 0) {
                    lockData.splice(index, 1)
                    lockData.splice(0, 0, this.defaultLockDataFillItem)
                    this.score += 1
                }
            })
            this.lockData = lockData.map(item => parseInt(item.join(''), 2))
            this.resetPrintData();
            if (this.score > 0 && this.score % 10 === 0) {
                this.speed += 1
            }
        },
        blockOnClick(x, y) {
            const arr = this.binary2Arr(this.printData)
            arr[y][x] = arr[y][x] === '1' ? '0' : '1'
            this.printData = this.arr2Binary(arr).map(item => parseInt(item, 2))
        },
        binary2Arr(binaryArr) {
            return binaryArr.map(item => item.toString(2).padStart(binaryArr.length, '0').split(""))
        },
        arr2Binary(arr) {
            return arr.map(item => item.join("").toString(2).padStart(arr.length, '0'))
        },
        binary2int(binaryArr) { 
            return binaryArr.map(item => parseInt(item, 2))
        },
        rollLeftArr(arr) {
            return arr[0].map((item, index) => {
                return arr.map(mapItem => mapItem[index])
            })
        },
        rollRightArr(arr) {
            return arr[0].map((item, index) => {
                return arr.map(mapItem => mapItem[index])
            })
        },
        bitwiseArr(arr, direction, step = 1) {
            if (!Array.isArray(arr[0])) {
                console.warn('bitwiseArr 格式不正确', arr[0])
                return false;
            }
            let data = arr;
            for (let i = 0; i < step; i++) {
                if (direction === 'right') { // 1073741824 536870912, 939524096
                    const newData = data.map(item => (parseInt(item.join(""), 2)).toString(2).padStart(data.length, '0')).map(item => item.split(""))
                    if (!newData.map(item => item[item.length - 1]).includes('1')) {
                        data = data.map(item => (parseInt(item.join(""), 2) >> 1).toString(2).padStart(data.length, '0')).map(item => item.split(""))
                    }
                } else {
                    const newData = data.map(item => (parseInt(item.join(""), 2)).toString(2).padStart(data.length, '0')).map(item => item.split(""))
                    if (!newData.map(item => item[0]).includes('1')) {
                        data = data.map(item => (parseInt(item.join(""), 2) << 1).toString(2).padStart(data.length, '0')).map(item => item.split(""))
                    }
                }
            }
            return data;
        },
        createBlock() {
            this.printData = this.blocks[_.random(0, this.blocks.length - 1)]
        },
        roll() {
            if (this.lock) {
                return;
            }
            let arr = this.binary2Arr(this.printData)
            let original = this.printData
            let top = [];
            let right = [];
            arr.forEach((item, index) => {
                item.forEach((childItem, childIndex) => {
                    if (childItem === '1') {
                        top.push(index)
                        right.push(childIndex)
                    }
                })
            })
            const x = right[Math.floor(right.length / 2)]
            const y = top[Math.floor(top.length / 2)]
            arr = this.rollLeftArr(arr).reverse()
            let top2 = [];
            let right2 = [];
            arr.forEach((item, index) => {
                item.forEach((childItem, childIndex) => {
                    if (childItem === '1') {
                        top2.push(index)
                        right2.push(childIndex)
                    }
                })
            })
            const x2 = right2[Math.floor(right2.length / 2)]
            const y2 = top2[Math.floor(top2.length / 2)]

            const transX = x2 - x;
            const transY = y2 - y;

            this.printData = this.arr2Binary(arr).map(item => parseInt(item, 2))

            console.log(transX, transY);

            if (transX > 0) {
                this.left(Math.abs(transX), false)
            } else {
                this.right(Math.abs(transX), false)
            }
            if (transY > 0) {
                this.up(Math.abs(transY), false)
            } else {
                this.down(Math.abs(transY), false)
            }

            const lockData = this.binary2Arr(this.lockData);
            const newArr = this.binary2Arr(this.printData)
            let move = true;
            lockData.forEach((item, index) => {
                const finder = item.find((findItem, findIndex) => {
                    return findItem === newArr[index][findIndex] && findItem === '1'
                })
                if (finder) {
                    move = false;
                }
            })
            if (!move) {
                this.printData = original
            }
        },
        up(step = 1, check = true) {
            if (this.lock) {
                return;
            }
            let printData = [...this.printData];
            const binary2Arr = this.binary2Arr(printData)
            const rollLeftArr = this.rollLeftArr(binary2Arr)
            if (rollLeftArr.map(item => item[0]).includes('1')) {
                return;
            };
            const arr2Binary = this.arr2Binary(rollLeftArr)
            const bitwiseArr = this.bitwiseArr(this.binary2Arr(arr2Binary), 'left', step)
            const rollRightArr = this.rollRightArr(bitwiseArr)
            const lockData = this.binary2Arr(this.lockData);
            let move = true;
            lockData.forEach((item, index) => {
                const finder = item.find((findItem, findIndex) => {
                    return findItem === rollRightArr[index][findIndex] && findItem === '1'
                })
                if (finder) {
                    move = !check || false;
                }
            })
            if (move) {
                const arr2Binary3 = this.arr2Binary(rollRightArr)
                this.printData = arr2Binary3.map(item => parseInt(item, 2))
            } else {
                this.saveToLockData();
            }
        },
        down(step = 1, check = true) {
            if (this.lock) {
                return;
            }
            let printData = [...this.printData];
            const binary2Arr = this.binary2Arr(printData)
            const rollLeftArr = this.rollLeftArr(binary2Arr)
            if (rollLeftArr.map(item => item[item.length - 1]).includes('1')) {
                this.saveToLockData();
                return;
            };
            const arr2Binary = this.arr2Binary(rollLeftArr)
            const bitwiseArr = this.bitwiseArr(this.binary2Arr(arr2Binary), 'right', step)
            const rollRightArr = this.rollRightArr(bitwiseArr)
            const lockData = this.binary2Arr(this.lockData);
            let move = true;
            lockData.forEach((item, index) => {
                const finder = item.find((findItem, findIndex) => {
                    return findItem === rollRightArr[index][findIndex] && findItem === '1'
                })
                if (finder) {
                    move = !check || false;
                }
            })
            if (move) {
                const arr2Binary3 = this.arr2Binary(rollRightArr)
                this.printData = arr2Binary3.map(item => parseInt(item, 2))
            } else {
                this.saveToLockData();
            }

        },
        left(step = 1, check = true) {
            if (this.lock) {
                return;
            }
            if (this.binary2Arr(this.printData).map(item => item[0]).includes('1')) {
                return;
            }
            const printDataArr = this.bitwiseArr(this.binary2Arr(this.printData), 'left', step)
            let move = true;
            const lockData = this.binary2Arr(this.lockData);
            lockData.forEach((item, index) => {
                const finder = item.find((findItem, findIndex) => {
                    return findItem === printDataArr[index][findIndex] && findItem === '1'
                })
                if (finder) {
                    move = !check || false;
                }
            })
            if (move) {
                this.printData = this.binary2int(this.arr2Binary(this.bitwiseArr(this.binary2Arr(this.printData), 'left', step)))
            }
        },
        right(step = 1, check = true) {
            if (this.lock) {
                return;
            }
            if (this.binary2Arr(this.printData).map(item => item[item.length - 1]).includes('1')) {
                return;
            }
            const printDataArr = this.bitwiseArr(this.binary2Arr(this.printData), 'right', step)
            let move = true;
            const lockData = this.binary2Arr(this.lockData);
            lockData.forEach((item, index) => {
                const finder = item.find((findItem, findIndex) => {
                    return findItem === printDataArr[index][findIndex] && findItem === '1'
                })
                if (finder) {
                    move = !check || false;
                }
            })
            if (move) {
                this.printData = this.binary2int(this.arr2Binary(this.bitwiseArr(this.binary2Arr(this.printData), 'right', step)))
            }
        },
        checkScreen(tag = 1) {
            return new Promise(resolve => {
                const arr = this.binary2Arr(this.printData)
                const loopArr = (index) => { 
                    if (index < arr.length) {
                        setTimeout(() => { 
                            arr[index] = arr[index].map(() => tag ? '1' : '0')
                            this.printData = this.arr2Binary(arr).map(printItem => parseInt(printItem, 2))
                            loopArr(++index)
                        }, 16)
                    } else {
                         resolve()
                    }
                }
                loopArr(0)
            })
        },
        async refreshScreen() {
            this.lock = true;
            await this.checkScreen(1);
            this.resetLockData();
            await this.checkScreen(0);
            this.lock = false;
            this.isStart = false;
            this.speed = 1;
            this.score = 0;
        }
    },
    computed: {
        print() {
            const bit = this.printData.length
            const blocks = [];
            const printData = this.printData.map((value, index) => value | this.lockData[index]);
            const empty = Array.isArray(printData) ? printData : new Array(bit).fill(0)
            empty.forEach(item => {
                const arr = Number(item).toString(2).padStart(bit, '0').split("")
                blocks.push(arr)
            })
            return blocks;
        }
    },
    watch: {
        print() { 
            if (this.canvas) {
                const nowTimestamp = new Date().valueOf();
                if (nowTimestamp - this.drawTimestamp > (1000 / this.fps)) {
                    this.drawOnCanvas();
                    this.drawText();
                    this.drawTimestamp = new Date().valueOf();
                } else {
                    if (this.drawTimmer) {
                        clearTimeout(this.drawTimmer)
                    }
                    this.drawTimmer = setTimeout(() => { 
                         this.drawOnCanvas();
                         this.drawText();
                    }, 1000 / this.fps)
                }
            }
        },
        speed() { 
            this.drawOnCanvas();
            this.drawText();
        },
        score() { 
            this.drawOnCanvas();
            this.drawText();
        },
    },
}
</script>
<style scoped>
.main {
    border: 1px solid #000;
    display: inline-block;
}

.line {
    display: flex;
}

.block {
    width: 10px;
    height: 10px;
    box-sizing: border-box;
}

.block-0 {
    background: #fff;
    border: 1px solid #000;
}

.block-1 {
    background: #000;
    border: 1px solid #fff;
}
</style>