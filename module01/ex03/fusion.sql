ALTER TABLE public.customers
ADD COLUMN category_ids BIGINT[],
ADD COLUMN category_codes character varying(255)[],
ADD COLUMN brands character varying(255)[];


WITH non_null_items AS (
    SELECT 
        product_id,
        ARRAY_AGG(DISTINCT category_id) FILTER (WHERE category_id IS NOT NULL) AS category_ids,
        ARRAY_AGG(DISTINCT category_code) FILTER (WHERE category_code IS NOT NULL) AS category_codes,
        ARRAY_AGG(DISTINCT brand) FILTER (WHERE brand IS NOT NULL) AS brands
    FROM public.items
    GROUP BY product_id
)

UPDATE public.customers AS customers
SET
    category_ids = non_null_items.category_ids,
    category_codes = non_null_items.category_codes,
    brands = non_null_items.brands
FROM non_null_items
WHERE customers.product_id = non_null_items.product_id;