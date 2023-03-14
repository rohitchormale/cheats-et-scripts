/*
struct is typed collection of records.
structs are mutable.
On struct type, methods can be defined on value or pointer receiver.
*/
package main


import "fmt"

type name struct {
	fname string
	lname string
}

type person struct {
	name
	age int
}

func (p person) FullName() string {
	return p.fname + " " + p.lname
}

func (p *person) Age() int {
	// pointer gets de-referenced automatically
	return p.age
}

func main() {
	// embedded struct
	p := person{
		name: name{"joe", "smith"},
		age: 100,
	}
	fmt.Println(p.name)
	fmt.Println(p.name.fname)
	fmt.Println(p.name.lname)
	fmt.Println(p.age)

	// method on value receiver
	fmt.Println("\n--- method on value receiver ---")
	fmt.Println(p.FullName())
	fmt.Println(p.Age())

	// method on pointer receiver
	fmt.Println("\n--- method on pointer receiver ---")
	rp := &p
	fmt.Println(rp.FullName())
	fmt.Println(rp.Age())
}