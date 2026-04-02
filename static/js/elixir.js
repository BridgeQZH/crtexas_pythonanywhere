// static/js/elixir.js
// 卡牌圣水花费映射：elixirCost[cardIndex] = 圣水费用（整数）
// cardIndex 对应 game.html 里 data-id 的值（0-119）
// 当前为占位数据（1-9循环），请根据实际卡牌替换每个值。
// 对应关系见 cardmap.js 中的 idMapping 数组：
//   cardIndex 0 → idMapping[0] = "26000072" (Archer Queen)
//   cardIndex 1 → idMapping[1] = "26000001" (Archers)
//   ... 以此类推

const elixirCost = [
//  0   1   2   3   4   5   6   7   8   9
    5,  3,  3,  4,  5,  3,  2,  6,  5,  2,  // 0-9
    4,  4,  2,  4,  2,  6,  5,  3,  5,  3,  // 10-19
    4,  3,  3,  5,  7,  1,  4,  6,  6,  3,  // 20-29
    5,  1,  4,  3,  3,  4,  4,  4,  5,  6,  // 30-39
    3,  4,  2,  4,  4,  3,  6,  4,  5,  2,  // 40-49
    5,  4,  8,  5,  3,  1,  4,  4,  2,  1,  // 50-59
    3,  4,  5,  3,  7,  6,  3,  4,  4,  7,  // 60-69
    3,  4,  3,  4,  5,  3,  1,  5,  4,  4,  // 70-79
    4,  4,  7,  4,  4,  5,  3,  2,  5,  5,  // 80-89
    6,  3,  3,  6,  5,  7,  4,  3,  3,  4,  // 90-99
    4,  1,  2,  6,  2,  6,  2,  4,  2,  9,  // 100-109
    3,  3,  4,  3,  2,  5,  5,  6,  2,  4   // 110-119
];

/**
 * 获取卡牌圣水费用
 * @param {number|string} cardIndex 0-119
 * @returns {number}
 */
function getElixir(cardIndex) {
  const i = Number(cardIndex);
  return (i >= 0 && i < elixirCost.length) ? elixirCost[i] : 3;
}

window.elixirCost = elixirCost;
window.getElixir  = getElixir;
