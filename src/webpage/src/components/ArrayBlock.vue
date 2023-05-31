<script setup></script>
<template>
    <div>
        <div class="main">
            <div class="line" v-for="(item,y) in print" :key="y">
                <div class="block" :class="o === '0' ? 'block-0': 'block-1'" v-for="(o, x) in item" :key="x" @click="blockOnClick(x, y)">
                </div>
            </div>
        </div>
        <div>{{ printData }}</div>
        <div>{{ lockData }}</div>
        <button @click="up">up</button>
        <button @click="down">down</button>
        <button @click="left">left</button>
        <button @click="right">right</button>
        <button @click="saveToLockData">saveToLockData</button>
    </div>
</template>
<script>
export default {
    name: 'ArrayBlock',
    data() { 
        return {
            bitWidth: 16,
            printData: [],
            lockData: []
        }
    },
    created() { 
        this.initData();
        this.lockData = new Array(this.bitWidth).fill(0)
    },
    methods: {
        initData() { 
            this.printData = new Array(this.bitWidth).fill(0)
        },
        saveToLockData() { 
            const printData = this.binary2Arr(this.printData);
            const lockData = this.binary2Arr(this.lockData);
            printData.forEach((item, y) => {
                item.forEach((pix, x) => { 
                    lockData[y][x] = lockData[y][x] === '1' ? lockData[y][x] : printData[y][x]
                })
            })
            this.lockData = lockData.map(item => parseInt(item.join(''), 2))
            this.initData();
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
        bitwiseArr(arr, direction) { 
            if (direction === 'right') {
                return arr.map(item => (parseInt(item, 2) >> 1).toString(2))
            } else {
                return arr.map(item => (parseInt(item, 2) << 1).toString(2))
            }
        },
        up() { 
            let printData = [...this.printData];
            const binary2Arr = this.binary2Arr(printData)
            const rollLeftArr = this.rollLeftArr(binary2Arr)
            if (rollLeftArr.find(item => item[0] != 0)) {
                return;
            };
            const arr2Binary = this.arr2Binary(rollLeftArr)
            const bitwiseArr = this.bitwiseArr(arr2Binary, 'left')
            const binary2Arr2 = this.binary2Arr(bitwiseArr)
            const rollRightArr = this.rollRightArr(binary2Arr2)
            const arr2Binary3 = this.arr2Binary(rollRightArr)
            this.printData = arr2Binary3.map(item => parseInt(item, 2))
        },
        down() { 
            let printData = [...this.printData];
            const binary2Arr = this.binary2Arr(printData)
            const rollLeftArr = this.rollLeftArr(binary2Arr)
            if (rollLeftArr.find(item => item[item.length - 1] != 0)) {
                return;
            };
            const arr2Binary = this.arr2Binary(rollLeftArr)
            const bitwiseArr = this.bitwiseArr(arr2Binary, 'right')
            const binary2Arr2 = this.binary2Arr(bitwiseArr)
            const rollRightArr = this.rollRightArr(binary2Arr2)
            const arr2Binary3 = this.arr2Binary(rollRightArr)
            this.printData = arr2Binary3.map(item => parseInt(item, 2))
        },
        left() { 
            const printDataArr = this.printData.map(item => item.toString(2).padStart(this.printData.length, '0').split(""))
            if (printDataArr.map(item => item[0]).find(item => item > 0)) {
                return;
            }
            this.printData = this.printData.map(item => item << 1)
        },
        right() { 
            const printDataArr = this.printData.map(item => item.toString(2).padStart(this.printData.length, '0').split(""))
            if (printDataArr.map(item => item.pop()).find(item => item > 0)) {
                return;
            }
            this.printData = this.printData.map(item => item >> 1)
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
        border: 1px solid #000;
        display: inline-block;
    }
    .line {
        display: flex;
    }
    .block {
        width: 10px;
        height: 10px;
        border: 1px solid #000;
    }
    .block-0 {
        background: #fff;
    }
    .block-1 {
        background: #000;
    }
</style>