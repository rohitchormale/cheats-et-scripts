    

## Documentation

### Using ri ( ruby index) and RDoc ( Ruby Documentation)


    # If using rvm
    rvm docs generate ( or rvm docs generate-ri)
    # If not using rvm
    gem install rdoc-data
    rdoc-date --install
    # then see docs in your shell, using ri command
    ri Hash
    # Alternatively you can run 'ri' command in ruby interpreter like irb or pry


## Comments

### Single line


    # This is single line comment.
    # Added one more comment line
    # Enough comments


### Multiline comments


    =begin
    This is multiline comment.
    This style is rarely used.
    =end


# Built-in DataTypes #


## String ##

    # New string 
    s = String.new #=> ""
    s = String.new("foo") #=> "foo"
    s = String.new('foo') #=> 'foo'
    s = ""
    s = "foo bar baz"
    
    # Notation
    ## Can use both single quote or double quote to represnt strings
    ## Prefer double quotes as they support string interpolation
    
    # Interpolation
    ## var
    name ="foo"
    "hello world ! I am #{name}"

    ## arithmetic operations
    "count is #{3 + 3}"#=> count is 6

    ## We can ommit curly braces if interpolated expression is reference to global var, instant var or class var 
    @instance_var = "foo"
    "#@instance_var bar!"

    @class_var = "foo"
    "#@class_var bar!"

    $global_var = "foo"
    "#@global_var bar !"

    # Combine strings
    ## using + operator
    "foo" + "bar"
    "foo" + "3".to_s
    
    ## repeated string using * operator
    "foo" * 3
    
    ## concat strings
    "foo ".concat("bar ").concat("baz ")
    
    ## Append to string
    "foo" << " bar"
   
    # String conversation
    3.to_s

    # Cases
    s.upcase
    s.downcase
    s.capitalize
    s.swapcase
    
    # Other useful methods
    s.length
    s.reverse
    s.chars #=> gives array of all chars 
    
    # Split
    "foo bar".split #=> 
    "foo bar".split(" ")
    "foo bar".split(/ /)
    "foo bar".split(//) #=> ["f", "o", "o", " ", "b", "a", "r"] 
    first, *remaining = s.split(/,/)
    
    # gsub 
    ## gsub(pattern, replacement) or gusb(pattern)




## Array


### Creation/Initialization


    # Empty array
    array = Array.new
    array = a[]
    array = a.[]
    
    # Array with items
    array = Array.new([1, 2, 'foo'])
    array = [1, 2, 3, 'foo']
    
    # Array with specific length
    array = Array.new(3)
    
    # Array with specific length and default values
    array = Array.new(3, 'foo')



### Insert/Add

    
    # Add a single item at last
    array << 'foo'
    
    # Add multiple items at last
    array.push(3)
    array.push(3, 4, 5)
    array.push 3, 4, 5
    
    # Add items at specific position
    array.insert(0, 'foo')
    array.insert(-3, 'foo')



### Remove/Delete


    # Remove last item & return it
    array.pop # Returns item 
    
    # Remove last 3 items and return them in array
    array.pop(3)
    
    # Delete item by it's position and return deleted item 
    array.delete_at(3)
    
    # Delete item by value and return it
    # If multiple occurance of same item present, delete them all but only return single item
    array.delete("foo")
    
    # Delete using '-' operator if only all array items are of same types
    array = [1, 2, 3, 4, 1]
    array - [3, 4]


### Accessing

    
    # Access first item from begining (left side) 
    array[0]
    array.first
    
    # Access first item from last (right side)
    array[-1]
    array.last
    
    # Access other items using indices
    array[2]
    array[-3]
    
    # Access items using range
    array[1, 3]
    array[1..3]
    
    # See length of array 
    array.length
    
    # Reverse array
    array.reverse
    
    # Check if item present in array
    array.include?('foo')


## Hashes


### Creation


    # Empty Hash
    h = Hash.new
    h = {}

    # Hash with items
    h = { "foo": "bar", "baz": 1}


### Add


    h["foo"] = "bar"
    # Add items by merging 2 hashes
    h.merge!{ "foo" => "bar"} # only `merge` instead `merge!` returns new hash without modifying old hash


### Remove


    h.delete("foo")


### Notation


    {"foo" => 1} # Here key `foo` is string
    {:foo => 1} # Here key `foo` is symbol
    # If all keys in hash are symbols, ruby provides alternative syntax
    {foo: 1, bar: 2}

    # In ruby 2.3.x, in all follownig cases, key is symbol
    {:"foo" => 1}
    {"foo": 1}
    {:foo => 1}
    {foo: 1}
    
    
### Accessing


    h.[](foo)
    h.[] "foo"
    h["foo"] # syntactic sugar
    h[:foo] # when key is symbol
    h.include?("foo")
    h.length
    # array of all keys
    h.keys
    # array of all values
    h.values
    # existence of key
    h.key?("foo")
    # existence of value
    h.key?("bar")

   
        
