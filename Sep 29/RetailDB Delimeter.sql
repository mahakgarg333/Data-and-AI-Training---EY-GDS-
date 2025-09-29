Delimiter $$
create procedure getAllProducts()
begin
	select product_id, product_name, category, price
    from productss;
end$$
 
Delimiter ;
call getAllProducts();