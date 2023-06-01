<script setup></script>
<template>
    <div>
        <div class="main">
            <div class="line" v-for="(item, y) in print" :key="y">
                <div class="block" :class="o === '0' ? 'block-0' : 'block-1'" v-for="(o, x) in item" :key="x"
                    @click="blockOnClick(x, y)">
                </div>
            </div>
        </div>
        <div>{{ isStart }}</div>
        <div>{{ printData }}</div>
        <div>{{ lockData }}</div>
        <button @click="createBlock">createBlock</button>
        <button @click="up(1, true)">up</button>
        <button @click="down(1, true)">down</button>
        <button @click="left(1, true)">left</button>
        <button @click="right(1, true)">right</button>
        <button @click="roll">roll</button>
        <button @click="saveToLockData">saveToLockData</button>
        <button @click="refreshScreen">refreshScreen</button>
        <button @click="start">start</button>
        <button @click="lock = !lock">lock</button>
    </div>
</template>
<script>
import * as _ from 'lodash'
export default {
    name: 'ArrayBlock',
    data() {
        return {
            isStart: false,
            lock: false,
            bitWidth: 31, // max 31
            printData: [],
            lockData: [],
            blocks: [
                // [98304, 49152, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                // [32768, 114688, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                // [98304, 98304, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                // [32768, 32768, 32768, 32768, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                // [65536, 98304, 32768, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [98304, 32768, 32768, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                // [49152, 32768, 32768, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                // [196608, 65536, 98304, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                // [32768, 98304, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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
    methods: {
        start() {
            if (this.lock) {
                return;
            }
            this.isStart = true;
            const timmer = setInterval(() => {
                if (this.lockData.filter(item => !item).length === 0) {
                    this.isStart = false;
                    clearInterval(timmer);
                    return;
                }
                this.down(1, true)
                if (!this.printData.find(item => !!item)) {
                    this.createBlock()
                }

            }, 100)
        },
        resetPrintData() {
            this.printData = new Array(this.bitWidth).fill(0)
        },
        resetLockData() {
            this.lockData = new Array(this.bitWidth).fill(0)
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
                    lockData = [].concat([new Array(this.bitWidth).fill('0')], lockData)
                }
            })
            this.lockData = lockData.map(item => parseInt(item.join(''), 2))
            this.resetPrintData();
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
            let data = arr;
            for (let i = 0; i < step; i++) {
                if (direction === 'right') {
                    data = arr.map(item => (parseInt(item, 2) >> step).toString(2).padStart(arr.length, '0'))
                } else {
                    data = arr.map(item => (parseInt(item, 2) << step).toString(2).padStart(arr.length, '0'))
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
            console.log(top, right, top.map((item, index) => [, right[index]]));
            console.log(x, y);
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
            if (rollLeftArr.find(item => item[0] != 0)) {
                return;
            };
            const arr2Binary = this.arr2Binary(rollLeftArr)
            const bitwiseArr = this.bitwiseArr(arr2Binary, 'left', step)
            const binary2Arr2 = this.binary2Arr(bitwiseArr)
            const rollRightArr = this.rollRightArr(binary2Arr2)
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
            }
        },
        down(step = 1, check = true) {
            if (this.lock) {
                return;
            }
            let printData = [...this.printData];
            const binary2Arr = this.binary2Arr(printData)
            const rollLeftArr = this.rollLeftArr(binary2Arr)
            if (rollLeftArr.find(item => item[item.length - 1] != 0)) {
                this.saveToLockData();
                return;
            };
            const arr2Binary = this.arr2Binary(rollLeftArr)
            const bitwiseArr = this.bitwiseArr(arr2Binary, 'right', step)
            const binary2Arr2 = this.binary2Arr(bitwiseArr)
            const rollRightArr = this.rollRightArr(binary2Arr2)
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
            if (this.binary2Arr(this.printData).map(item => item[0]).find(item => item > 0)) {
                return;
            }
            const printDataArr = this.binary2Arr(this.printData.map(item => item << step))
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
                this.printData = this.printData.map(item => item << step)
            }
        },
        right(step = 1, check = true) {
            if (this.lock) {
                return;
            }
            if (this.binary2Arr(this.printData).map(item => item.pop()).find(item => item > 0)) {
                return;
            }
            const printDataArr = this.binary2Arr(this.printData.map(item => item >> step))
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
                this.printData = this.printData.map(item => item >> step)
            }
        },
        checkScreen(tag = 1) {
            return new Promise(resolve => {
                const arr = this.binary2Arr(this.printData)
                const loop = (list, index) => {
                    const pm = () => new Promise(resolve => {
                        const loopLine = (childIndex) => {
                            if (childIndex < list[index].length) {
                                setTimeout(() => {
                                    arr[index][childIndex] = tag ? '1' : '0'
                                    this.printData = this.arr2Binary(arr).map(printItem => parseInt(printItem, 2))
                                    loopLine(++childIndex)
                                }, 1)
                            } else {
                                resolve(true)
                            }
                        }
                        loopLine(0)
                    })
                    pm().then(() => {
                        if (index < list.length - 1) {
                            loop(list, ++index)
                        } else {
                            resolve()
                        }
                    })
                }
                loop(arr, 0)
            })
        },
        async refreshScreen() {
            this.lock = true;
            await this.checkScreen(1);
            this.resetLockData();
            await this.checkScreen(0);
            this.lock = false;
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
    }
}
</script>
<style scoped>
.main {
    border: 1px solid #3e83bd;
    display: inline-block;
}

.line {
    display: flex;
}

.block {
    width: 10px;
    height: 10px;
}

.block-0 {
    background: #fff;
    border: 1px solid #3e83bd;
}

.block-1 {
    background: #3e83bd;
    border: 1px solid #fff;
}
</style>