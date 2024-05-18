var v = 2;
let l =3;
const c =4;
{
  var v = 20;
  let l = 30;
  const c = 40;
  console.log(v);
  console.log(l);
  console.log(c);
}
function test(){
  var v = 20;
  let l = 30;
  const c = 40;
  console.log(v);
  console.log(l);
  console.log(c);
}
test();
console.log(v);
console.log(l);
console.log(c);